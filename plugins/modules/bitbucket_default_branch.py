#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_default_branch
short_description: Update the default branch of a repository
description:
- Set the default branch of a repository.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski
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
  branch:
    description:
    - Branch name to set as default
    type: str
    default: develop
    required: true  
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
- name: Update the default branch of a repository
  esp.bitbucket.bitbucket_default_branch:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    branch: develop
'''

RETURN = r'''
project_key:
    description: Bitbucket project key.
    returned: always
    type: str
    sample: FOO
repository:
    description: Bitbucket repository name.
    returned: always
    type: str
    sample: bar      
branch:
    description: Branch name to set as default.
    returned: always
    type: str
    sample: master
isDefault:
    description: Whether the branch is a default branch for the supplied repository.
    returned: success
    type: bool
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        branch=dict(type='str', default='develop'),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    branch = module.params['branch']
    project_key = module.params['project_key']
    repository = module.params['repository']        

    # Seed the result dict in the object
    result = dict(
        changed=False,
        isDefault=True,
        project_key=project_key,
        repository=repository,
        branch=branch,
        json={},
    )

    # Check if project exists.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        module.fail_json(msg='Project `{projectKey}` does not exist.'.format(
            projectKey=project_key,
        ))      

    # Check if repository exists.
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=project_key, repository=repository):
        module.fail_json(msg='Repository `{repository}` does not exist.'.format(
            repository=repository,
        ))      

    # Retrieve existing branches information (if any)
    existing_branches = bitbucket.get_branches_info(fail_when_not_exists=False, filter=None)

    # Check if the supplied branch exists
    if any(d.get('displayId', 'non_existing_branch') == branch for d in existing_branches):
        # Update the default branch of a repository, if the supplied branch exists and is not set as default one
        if not any(d.get('displayId', 'non_existing_branch') == branch and d.get('isDefault', False) for d in existing_branches):
            if not module.check_mode:
                result['json'] = bitbucket.set_default_branch(branch=branch)
            result['changed'] = True
    else:
        module.fail_json(msg='Branch `{branch}` does not exist in `{repositorySlug}` repository'.format(
            branch=branch,
            repositorySlug=repository,
        ))

    module.exit_json(**result)

if __name__ == '__main__':
    main()