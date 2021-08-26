#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_application_link_info
short_description: Manage application links on Bitbucket Server
description:
- Manage application links on Bitbucket Server.
- One may refer to an application link either by its ID or its name.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
version_added: 1.2.0
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
  password:
    description:
    - Password used for authentication.
    - This is only needed when not using I(token).
    - Required when I(username) is provided.
    type: str
    required: false
  token:
    description:
    - Token parameter for authentication.
    - This is only needed when not using I(username) and I(password).
    type: str
    required: false
  applink:
    description:
    - Retrieve application links matching the supplied I(applink) filter.
    - This can be '*' which means all application links.
    - One may refer to an application link either by its ID or its name.    
    type: list
    required: false
    default: [ '*' ]
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
- Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Create application link
  esp.bitbucket.bitbucket_application_link:
    url: 'https://bitbucket.example.com'
    username: '{{ bitbucket_username }}'
    password: '{{ bitbucket_password }}'
    applink:
      name: FOO
      rpcUrl: https://terraform.example.com/app/my-org
      displayUrl: https://terraform.example.com/app/my-org
      key: "de00c96434df2b31d3e3e3164391091c"
      publicKey: |
        -----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0E6OBvxPXTQlyQ8IBIP7
        (...)
        Gzr9C9mYr5zh15Rd7ygubYT1rKPTnQEuQMZpki9rsS3cKEYGyIX6nFLJdpZHK7hL
        2QIDAQAB
        -----END PUBLIC KEY-----        
    state: present
    validate_certs: no
  register: _result

- name: Delete application link (supplied by name or ID)
  esp.bitbucket.bitbucket_application_link:
    url: 'https://bitbucket.example.com'
    username: '{{ bitbucket_username }}'
    password: '{{ bitbucket_password }}'
    applink:
      name: FOO
      #id: 227dd1d7-f6d6-34a5-b046-5663fb518691
    state: absent
    validate_certs: no
'''

RETURN = r'''
json:
    description: Details of application link.    
    returned: success
    type: dict
    sample:        
        id: "227dd1d7-f6d6-34a5-b046-5663fb518691"
        status:
            resources-created:
                link:
                    "@href": "https://bitbucket.example.com/rest/applinks/3.0/applicationlink/227dd1d7-f6d6-34a5-b046-5663fb518691"
                    "@rel": "self"
            status-code: "201"            
'''

import re
import xmltodict
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def create_application_link(module, bitbucket, data=None):
    """
    Create Application Link

    """
    if 'name' not in module.params['applink']:
        module.fail_json(msg='`applink.name` is required when the `state` is `present`')
    if 'rpcUrl' not in module.params['applink']:
        module.fail_json(msg='`applink.rpcUrl` is required when the `state` is `present`')        
    if 'displayUrl' not in module.params['applink']:
        module.fail_json(msg='`applink.displayUrl` is required when the `state` is `present`')        

    data = {
        'id': None,
        'name': module.params['applink']['name'],
        'rpcUrl': module.params['applink']['rpcUrl'],
        'displayUrl': module.params['applink']['displayUrl'],
        'typeId': 'generic'
    }

    info, content = bitbucket.request(
        api_url='{url}/rest/applinks/3.0/applicationlink'.format(url=module.params['url']),
        method='PUT',
        data=data,
    )

    if info['status'] == 201:        

        try:
            js = json.loads(json.dumps(xmltodict.parse(content['content'])))
            if isinstance(js, dict):
                m = re.search('applicationlink/(.+?)"', content['content'])
                if m:
                    js['id'] = m.group(1)
            ret = js
        except Exception as e:
            ret = content
            
        return ret

    if info['status'] != 201:
        module.fail_json(msg='Failed to create an application link: {info}'.format(
            info=info,
        ))

    return None


def update_application_link(module, bitbucket, applicationLinkID=None, data=None):
    """
    Update Application Link

    """
    if 'key' not in module.params['applink']:
        module.fail_json(msg='`applink.key` is required when the `state` is `present`')
    if 'name' not in module.params['applink']:
        module.fail_json(msg='`applink.name` is required when the `state` is `present`')        
    if 'publicKey' not in module.params['applink']:
        module.fail_json(msg='`applink.publicKey` is required when the `state` is `present`')        

    data = {
        'key': module.params['applink']['key'],
        'name': module.params['applink']['name'],
        'description': module.params['applink'].get('description', None),
        'sharedSecret': module.params['applink'].get('sharedSecret', None),
        'publicKey': module.params['applink']['publicKey'],
        'outgoing': module.params['applink'].get('outgoing', False),
        'twoLOAllowed': module.params['applink'].get('twoLOAllowed', False),
        'executingTwoLOUser': module.params['applink'].get('executingTwoLOUser', None),
        'twoLOImpersonationAllowed': module.params['applink'].get('twoLOImpersonationAllowed', None),
    }

    info, content = bitbucket.request(
        api_url='{url}/rest/applinks-oauth/1.0/applicationlink/{applicationLinkID}/authentication/consumer'.format(
            url=module.params['url'],
            applicationLinkID=applicationLinkID,
        ),
        method='PUT',
        data=data,
    )

    if info['status'] == 201:            
        try:
            js = json.loads(json.dumps(xmltodict.parse(content['content'])))
            if isinstance(js, dict):
                m = re.search('applicationlink/(.+?)/', content['content'])
                if m:
                    js['id'] = m.group(1)
            ret = js
        except Exception as e:
            ret = content
            
        return ret

    if info['status'] != 201:
        module.fail_json(msg='Failed to update an application link: {info}'.format(
            info=info,
        ))

    return None


def delete_application_link(module, bitbucket, id=None, fail_when_not_exists=False):
    """
    Delete Application Link

    """
    url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['applinks'] + '/{id}').format(
                    url=module.params['url'],
                    id=id,
        )

    info, content = bitbucket.request(
        api_url=url,
        method='DELETE',
    )

    if info['status'] == 204:        
        return content        

    if info['status'] != 204:
        if fail_when_not_exists:
            module.fail_json(msg='Failed to delete an application link: {info}'.format(
                info=info,
            ))
        else:
            return { 
                'id': id,
                'status': info['status'],
                'info': info,
                'deleted': False,
            }

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        applink=dict(type='dict', required=True, no_log=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')],
    )

    bitbucket = BitbucketHelper(module)

    module.params['return_content'] = True

    state = module.params['state']
    applink = module.params['applink']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        state=state,
        json={},
    )
    if state == 'absent':
        result['applink'] = applink

    # Retrieve detalis on all Application Links
    all_applinks = bitbucket.get_application_links_info()

    found = [al for al in all_applinks['json'] if al['id'] == applink.get('id', '_') or al['name'] == applink.get('name', '_')]

    if len(found) > 1:
        module.fail_json(msg='Found multiple Application Links matching the supplied parameter "%s". Refer to application link either by its ID or name.' % (applink) )

    # Delete application link when it exists and state == 'absent'
    if state == 'absent':

          if len(found) == 1:
              result['changed'] = True
              if not module.check_mode:
                  result['json'] = delete_application_link(module, bitbucket, id=found[0]['id'], fail_when_not_exists=False )

    # Create or update application link when state == 'present'
    else:

          if len(found) == 0:
              result['changed'] = True
              if not module.check_mode:
                  result['json'] = create_application_link(module, bitbucket, data=applink)
                  update_application_link(module, bitbucket, applicationLinkID=result['json']['id'], data=applink)

          if len(found) == 1:
              result['changed'] = True
              if not module.check_mode:
                  result['json'] = update_application_link(module, bitbucket, applicationLinkID=found[0]['id'], data=applink)

    module.exit_json(**result)


if __name__ == '__main__':
    main()