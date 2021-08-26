#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_branch_permissions_info
short_description: Retrieve branch permissions
description:
- Search for branch restrictions for the supplied project or repository.
- A restriction means preventing writes on the specified branch by all except a set of users and/or groups, or preventing specific operations such as branch deletion.
- Authentication can be done with I(token) or with I(username) and I(password).
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
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ] 
  repository:
    description:
    - Repository name.
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
- Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Retrieve branch permissions for the supplied project
  esp.bitbucket.bitbucket_branch_permissions_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: FOO
    validate_certs: no

- name: Retrieve branch permissions for the supplied repository
  esp.bitbucket.bitbucket_branch_permissions_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: FOO
    repository: bar
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
    returned: always
    type: str
    sample: FOO
repository:
    description: Bitbucket repository name.
    returned: success
    type: str
    sample: bar  
restrictions:
    description: List of branch restrictions for the supplied project or repository.
    returned: always
    type: list
    elements: dict
    contains:
        matcher:
            description: Matcher description.
            returned: success
            type: dict
            sample:
                active: true
                displayId: Release
                id: RELEASE
                type:
                    id: MODEL_CATEGORY
                    name: Branching model category                    
        scope:
            description: Scope.
            returned: success
            type: dict
            sample:
                resourceId: 292
                type: PROJECT                                 
        groups:
            description: Bitbucket groups.
            returned: success
            type: list
            elements: str
            sample:
              - bitbucket-admin
        users:
            description: Bitbucket users.
            returned: success
            type: list
            elements: str
            sample:
              - joe
              - jsmith
        accessKeys:
            description: Bitbucket access keys.
            returned: success
            type: list
            elements: str
            sample: []
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=False, no_log=False),
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

    module.params['return_content'] = True

    project_key = module.params['project_key'] 
    repository = module.params['repository']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=project_key,
        restrictions=[],
        messages=[],
    )
    if repository is not None:
        result['repository'] = repository

    # Check if projects exist. Retrun message if it does not exist.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=project_key
        ))
    else:        
        # When repository name is supplied but it does not exists, then return with a message.
        if (repository is not None) and (not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=project_key, repository=repository)):
            result['messages'].append('Repository `{repository}` does not exist.'.format(
                repository=repository
            ))
        else:
            # Retrieve restrictions information
            result['restrictions'].extend(bitbucket.get_branch_permissions_info(fail_when_not_exists=False, project_key=project_key, repository=repository))

    module.exit_json(**result)


if __name__ == '__main__':
    main()