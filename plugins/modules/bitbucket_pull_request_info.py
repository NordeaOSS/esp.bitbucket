#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_pull_request_info
short_description: Get information about pull requests on Bitbucket Server
description:
- Get information about pull requests on Bitbucket Server.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Pawel Smolarz
version_added: 1.1.0
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
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]  
  return_content:
    description:
      - Whether or not to return the body of the response as a "content" key in
        the dictionary result no matter it succeeded or failed.
    type: bool
    default: true
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
- name: Get information about pull requests
  esp.bitbucket.bitbucket_pull_request_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
'''

RETURN = r'''
messages:
    description: List of error messages.
    returned: always
    type: list
    sample:
      - Project `FOOO` does not exist.
project_key:
    description: Bitbucket project key.
    returned: success
    type: str
    sample: FOO
repository:
    description: Bitbucket repository name.
    returned: success
    type: str
    sample: bar 
json:
    description: List of pull requests for the supplied project and repository.
    returned: success
    type: list
    elements: dict
    contains:
        author:
            description: Pull request author.
            returned: success
            type: str
            sample: john   
        title:
            description: Pull request title.
            returned: success
            type: str
            sample: baz.yml edited online with Bitbucket                
        fromRef:
            description: From branch name.
            returned: success
            type: str
            sample: develop
        toRef:
            description: To branch name.
            returned: success
            type: str
            sample: master     
        id:
            description: Pull request id.
            returned: success
            type: int
            sample: 2                      
        version:
            description: Pull request version.
            returned: success
            type: int
            sample: 0
        reviewers:
            description: List of reviewers.
            returned: success
            type: list
            elements: str
            sample:
              - joe
              - jsmith
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper

def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        repository=module.params['repository'],
        messages=[],
        json={},
    )

    # Check if project and repository exist. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))
        module.fail_json(msg=result['messages'])
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=module.params['repository']):
        result['messages'].append('Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=module.params['repository']
        ))
        module.fail_json(msg=result['messages'])

    # Retrieve existing pulls information (if any)
    existing_pulls = bitbucket.get_pull_request_info(fail_when_not_exists=False, filter=None)

    info_data = []
    for d in existing_pulls:
        info_data.append({'pull_id': d.get('id'), 'version': d.get('version'), 'author': d.get('author')['user']['name'],
                    'title': d.get('title'), 'fromRef': d.get('fromRef')['displayId'], 'toRef': d.get('toRef')['displayId']
                          , 'reviewers': d.get('reviewers')})

    result['json'] = info_data
    module.exit_json(**result)

if __name__ == '__main__':
    main()