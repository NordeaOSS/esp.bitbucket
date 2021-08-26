#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_directory_sync
short_description: Synchronise User Directories on Bitbucket Server
description:
- Synchronises User Directories on Bitbucket Server.
- Authentication should be done with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
version_added: 1.0.0
options:
  url:
    description:
    - Bitbucket Server URL.
    type: str
    required: false
  username:
    description:
    - Username used for authentication.
    - This is only needed when not using I(token).
    - Required when I(password) is provided.
    type: str
    required: false
    aliases: [ user ]
  password:
    description:
    - Password used for authentication.
    - This is only needed when not using I(token).
    - Required when I(username) is provided.
    type: str
    required: false
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated.
      - This should only set to C(no) used on personally controlled sites using self-signed certificates.
    type: bool
    default: yes
  use_proxy:
    description:
      - If C(no), it will not use a proxy, even if one is defined in an environment variable on the target hosts.
    type: bool
    default: yes 
  sleep:
    description:
      - Number of seconds to sleep between API retries.
    type: int
    default: 5
  retries:
    description:
      - Number of retries to call Bitbucket API URL before failure.
    type: int
    default: 3
notes:
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Synchronise User Directories
  esp.bitbucket.bitbucket_directory_sync:
    url: 'https://bitbucket.example.com'
    username: admin
    password: secrect
    validate_certs: no
'''

RETURN = r'''
user_directories_synced:
    description: List of synchronised User Directories.
    returned: success
    type: list
    contains:
        directoryId:
            description: Directory ID.
            returned: success
            type: int
            sample: 262145
        operation:
            description: Sync operation URL path.
            returned: success
            type: str
            sample: /plugins/servlet/embedded-crowd/directories/sync?directoryId=262145&atl_token=4731c4d872b4b4cf6e2d46a75061213d414a1af7
        info:
            description: Bitbucket API response info.
            returned: success
            type: dict
            sample:
                status: 200
                msg: OK (unknown bytes)
'''

import time
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import string_types
from ansible.module_utils.six.moves.urllib.parse import urlencode, urlsplit
from ansible.module_utils.common._collections_compat import Mapping, Sequence
from ansible.module_utils._text import to_native, to_text
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def kv_list(data):
    ''' Convert data into a list of key-value tuples '''
    if data is None:
        return None

    if isinstance(data, Sequence):
        return list(data)

    if isinstance(data, Mapping):
        return list(data.items())

    raise TypeError('cannot form-urlencode body, expect list or dict')


def form_urlencoded(data):
    ''' Convert data into a form-urlencoded string '''
    if isinstance(data, string_types):
        return data

    if isinstance(data, (Mapping, Sequence)):
        result = []
        for key, values in kv_list(data):
            if isinstance(values, string_types) or not isinstance(values, (Mapping, Sequence)):
                values = [values]
            for value in values:
                if value is not None:
                    result.append((to_text(key), to_text(value)))
        return urlencode(result, doseq=True)

    return data


def login_to_bitbucket_server(module, bitbucket):
    ''' Login to Bitbucket Server '''
    data = {
        'j_username': module.params['username'],
        'j_password': module.params['password'],
        '_atl_remember_me': 'on',
        'submit': 'Login',
    }
    if not isinstance(data, string_types):
        try:
            data = form_urlencoded(data)
        except ValueError as e:
            module.fail_json(msg='failed to parse body as form_urlencoded: %s' % to_native(e), elapsed=0)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    module.params['force_basic_auth'] = True
    module.params['return_content'] = True
    module.params['username'] = None
    module.params['password'] = None
    module.params['url_username'] = None
    module.params['url_password'] = None

    info, content = bitbucket.request(
        api_url=module.params['url'],
        method='POST',
        data=data,
        headers=headers,
    )
    
    if info['status'] == 200:
        return info
    else:
        module.fail_json(msg='Failed to login to Bitbucket server. Info: {info}'.format(
            info=info,
        ))

    return None


def get_user_directories_sync_operations(module, bitbucket, cookies_string):
    ''' Get Bitbucket User Directories sync operations '''
    headers = {
        'Cookie': cookies_string,
    }
    info, content = bitbucket.request(
        api_url=BitbucketHelper.BITBUCKET_API_ENDPOINTS['directories-list'].format(
            url=module.params['url'],
        ),
        method='GET',
        headers=headers,
    )

    if info['status'] == 200:
        return re.findall('(/plugins/servlet/embedded-crowd/directories/sync\?directoryId=\d+\&atl_token=[^"]+)', content['content'])
    else:
        module.fail_json(msg='Failed to get Bitbucket User Directories. Info: {info}'.format(
            info=info,
        ))

    return None


def synchronise_directory(module, bitbucket, cookies_string, operation):
    ''' Synchronise Bitbucket User Directory '''
    headers = {
        'Cookie': cookies_string,
    }
    info, content = bitbucket.request(
        api_url=module.params['url'] + operation,
        method='GET',
        headers=headers,
    )

    if info['status'] == 200:
        return info
    else:
        module.fail_json(msg='Failed to synchronise Bitbucket user directory. Operation: {operation}; Info: {info}'.format(
            operation=operation,
            info=info,
        ))

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
    )

    bitbucket = BitbucketHelper(module)

    changed = False
    content = {}

    info = login_to_bitbucket_server(module, bitbucket)
    cookies_string = info['cookies_string']

    sync_operations = get_user_directories_sync_operations(module, bitbucket, cookies_string)

    user_directories_synced = []
    for operation in sync_operations:
        try:
            directoryId = re.search('directoryId=(\d+)', operation).group(1)
        except AttributeError:
            directoryId = None
        info = {}

        if not module.check_mode:
            info = synchronise_directory(module, bitbucket, cookies_string, operation)

        user_directories_synced.append(dict(directoryId=int(directoryId), operation=operation, info=info))
        changed = True

    module.exit_json(changed=changed, user_directories_synced=user_directories_synced)


if __name__ == '__main__':
    main()