#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_branch_info
short_description: Retrieve branches information for the supplied project and repository
description:
- Retrieve branches information from Bitbucket Server for the supplied project and repository.
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
  branch:
    description:
    - Retrieve the branches matching the supplied I(branch) filter.
    - This can be '*' which means all branches.
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
- name: Retrieve all branches
  esp.bitbucket.bitbucket_branch_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no

- name: Retrieve the branches matching the supplied branch filters
  esp.bitbucket.bitbucket_branch_info:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    repository: bar
    project_key: FOO
    branch: [ develop, feature ]
    validate_certs: no
'''

RETURN = r'''
repository:
    description: Bitbucket repository name.
    returned: always
    type: str
    sample: bar
project_key:
    description: Bitbucket project key.
    returned: always
    type: str
    sample: FOO
messages:
    description: List of error messages.
    returned: always
    type: list
    sample:
      - Repository `bar2` does not exist. 
branches:
    description: List of repository branches.
    returned: always
    type: list
    contains:
        displayId:
            description: Branch display ID.
            returned: success
            type: str
            sample: feature/mybranch
        id:
            description: Branch ID.
            returned: success
            type: str
            sample: refs/heads/feature/mybranch
        isDefault:
            description: Whether or not the branche is default.
            returned: success
            type: bool
            sample: false
        type:
            description: Branch type.
            returned: success
            type: str
            sample: BRANCH
        latestChangeset:
            description: Latest Changeset id.
            returned: success
            type: str
            sample: 93b84625d75123b7f7942fd72225400fa66d62ec
        latestCommit:
            description: Latest Commit id.
            returned: success
            type: str
            sample: 93b84625d75123b7f7942fd72225400fa66d62ec
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False, aliases=['name']),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),        
        branch=dict(type='list', elements='str', no_log=False, default=[ '*' ]),
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

    # Parse `branch` parameter and create list of branches.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '*' which means all branches.
    branches = []
    branches = [p.strip() for p in module.params['branch']]
    branches = bitbucket.listify_comma_sep_strings_in_list(branches)
    if not branches:
        branches = [ '*' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        repository=module.params['repository'],
        project_key=module.params['project_key'],
        filter=branches,
        messages=[],
        branches=[],
    )

    # Check if project and repository exist. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=module.params['repository']):
        result['messages'].append('Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=module.params['repository']
        ))

    # Retrieve branches information if project and repository exist
    if not result['messages']:
        if '*' in branches:
            result['branches'] = bitbucket.get_branches_info(fail_when_not_exists=False, filter=None)
        else:
            for branch in branches:
                result['branches'].extend( bitbucket.get_branches_info(fail_when_not_exists=False, filter=branch) )

    module.exit_json(**result)


if __name__ == '__main__':
    main()