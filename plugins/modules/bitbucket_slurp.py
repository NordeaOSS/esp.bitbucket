#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_slurp
short_description: Slurps a file from Bitbucket Server
description:
- This module is used for fetching a base64-encoded blob containing the data in a file on Bitbucket Server.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
version_added: 1.0.0
options:
  src:
    description:
      - The file on the Bitbucket Server to fetch. This I(must) be a file, not a directory.
    type: path
    required: true
    aliases: [ path ]
  at:
    description:
    - The commit ID or ref (e.g. a branch or tag) to read a file at.
    - If not specified the default branch will be used instead.
    type: str
    required: false
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
  token:
    description:
    - Token parameter for authentication.
    - This is only needed when not using I(username) and I(password).
    type: str
    required: false
  repository:
    description:
    - Repository name.
    type: str
    required: true
    aliases: [ name ]
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]  
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
- This module returns an 'in memory' base64 encoded version of the file, take
    into account that this will require at least twice the RAM as the original file size.
- Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Read baz.yml file contents from Bitbucket Server from default branch
  esp.bitbucket.bitbucket_slurp:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    src: 'path/to/baz.yml'
    validate_certs: no
    force_basic_auth: yes
  register: _result

- name: Print returned information
  ansible.builtin.debug:
    msg: "{{ _result['content'] | b64decode }}"

- name: Read baz.yml file contents from Bitbucket Server from develop branch
  esp.bitbucket.bitbucket_slurp:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    repository: bar
    project_key: FOO
    src: 'path/to/baz.yml'
    at: develop
    validate_certs: no
  register: _result
'''

RETURN = r'''
content:
    description: Encoded file content
    returned: success
    type: str
    sample: "LS0tCmhlbGxvOiB3b3JsZAoK"
encoding:
    description: Type of encoding used for file
    returned: success
    type: str
    sample: "base64"
url:
    description: Actual URL of file slurped
    returned: success
    type: str
    sample: "https://bitbucket.example.com/rest/api/1.0/projects/FOO/repos/bar/raw/path/to/baz.yml"
'''

import base64

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


error_messages = {
    'insufficient_permissions_to_see': 'The currently authenticated user has insufficient permissions to see `{repositorySlug}` repository',
    'repository_does_not_exist': '`{repositorySlug}` repository does not exist',
 }


def slurp_file(module, bitbucket):
    """
    Read file content on Bitbucket Server

    """
    at = ""
    if module.params['at'] is not None:
        at = "?at=%s" % module.params['at']

    info, content = bitbucket.request(
        api_url=BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-raw-path'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['src'],
            at=at,
        ),
        method='GET',
    )

    if info['status'] == 200:
        content['content'] = base64.b64encode(content['content'].encode('utf-8')).decode('utf-8')
        content['encoding'] = 'base64'
        content['url'] = '{BitBucketApiURL}/projects/{projectKey}/repos/{repositorySlug}/browse/{path}{at}'.format(
            BitBucketApiURL=BitbucketHelper.BITBUCKET_API_URL,
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['src'],
            at=at,
        )
        return content

    if info['status'] != 200:
        module.fail_json(msg='Failed to retrieve content of a file which matches the supplied projectKey `{projectKey}`, repositorySlug `{repositorySlug}` and file path `{path}`: {info}'.format(
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['src'],
            info=info,
        ))

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False, aliases=['name']),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        src=dict(type='path', required=True, aliases=['path']),
        at=dict(type='str', required=False, no_log=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    content = {}

    # Slurp file
    #if get_existing_repository(module, bitbucket) is not None:
    if bitbucket.get_repository_info(fail_when_not_exists=True, project_key=module.params['project_key'], repository=module.params['repository']) is not None:
        content = slurp_file(module, bitbucket)

    module.exit_json(**content)


if __name__ == '__main__':
    main()