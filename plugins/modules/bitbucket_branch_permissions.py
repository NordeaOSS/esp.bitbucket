#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_branch_permissions
short_description: Manage restrictions for repository branches.
description:
- Create a restriction for the supplied branch to be applied on the given repository or all repositories in the given project.
- A restriction means preventing writes on the specified branch by all except a set of users and/or groups, or preventing specific operations such as branch deletion.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
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
    required: false
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]  
  branch_name:
    description:
    - A specific branch name you want to restrict access to.
    - This is only needed when not using I(branch_pattern) and I(branching_model).
    - One of I(branch_name), I(branch_pattern) and I(branching_model) is required.
    type: str
    required: false
  branch_pattern:
    description:
    - A wildcard pattern that may match multiple branches you want to restrict access to.
    - This is only needed when not using I(branch_name) and I(branching_model).
    - One of I(branch_name), I(branch_pattern) and I(branching_model) is required.
    type: str
    required: false
  branching_model:
    description:
    - Branch prefixes in the Branching model. Select the branch type you want to restrict access to.
    - This is only needed when not using I(branch_name) and I(branch_pattern).
    - One of I(branch_name), I(branch_pattern) and I(branching_model) is required.
    type: str
    choices: [ feature, bugfix, hotfix, release, development, production ]
    required: false
  restrictions:
    description:
      - Definition of the restrictions for repository branches.
    type: list
    suboptions:
      prevent:
        description:
        - Restriction name.
        type: str
        choices: [ 'deletion', 'rewriting history', 'changes without a pull request', 'all changes' ]
        required: true    
      exemptions:
        description:
        - Exemptions from the supplied restriction.
        type: dict             
        suboptions:
          groups:
            description:
            - Groups excluded from the restriction.
            type: list         
          users:
            description:
            - Users excluded from the restriction.
            type: list
          access_keys:
            description:
            - Access keys excluded from the restriction.
            type: list   
  state:
    description:
    - Whether the restriction should exist or not.
    type: str
    default: present
    choices: [ absent, present ]
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
- name: Create restrictions for the supplied branch
  esp.bitbucket.bitbucket_branch_permissions:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    branch_name: master
    restrictions:
      - prevent: deletion
      - prevent: rewriting history
        exemptions:
          groups: [ group1, group2 ]
          users: [ amy ]
          access_keys: []
      - prevent: changes without a pull request
        exemptions:
          groups: [ group3 ]
          users: [ joe ]
          access_keys: []                    
    state: present
    validate_certs: no

- name: Create restrictions for the supplied branches - bugfix branches - on all repositories in the given project
  esp.bitbucket.bitbucket_branch_permissions:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: FOO
    branching_model: bugfix
    restrictions:
      - prevent: all changes
        exemptions:
          groups: [ group1, group2 ]
          users: [ amy ]
          access_keys: []
    state: present
    validate_certs: no

- name: Create restrictions for the supplied branches - matching branch_pattern - on the given repository
  esp.bitbucket.bitbucket_branch_permissions:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    branch_pattern: develop
    restrictions:
      - prevent: deletion
      - prevent: changes without a pull request
        exemptions:
          groups: [ group4 ]
          users: [ john ]
    state: present
    validate_certs: no

- name: Delete restrictions for the supplied branch
  esp.bitbucket.bitbucket_branch_permissions:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: FOO    
    repository: bar  
    branch_name: master
    restrictions:
      - prevent: 'deletion'
        exemptions:
          groups: []
          users: [ john ]
          access_keys: []        
      - prevent: 'rewriting history'
    state: absent
    validate_certs: no
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
branch_name:
    description: A specific branch name.
    returned: success
    type: str
    sample: master
branch_pattern:
    description: A wildcard pattern that may match multiple branches.
    returned: success
    type: str
    sample: develop
branching_model:
    description: Branch prefixes in the Branching model.
    returned: success
    type: str
    sample: bugfix
results:
    description: List of affected branch permissions.
    returned: success
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
        id:                    
            description: Permission ID.
            returned: success
            type: int
            sample: 42                  
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


def create_branch_permission(module, bitbucket, project_key=None, repository=None, restriction_type=None, matcher=None, users=None, groups=None, accessKeys=None):
    """
    Create branch restrictions for the supplied project or repository.

    """

    if repository is None:
        url = BitbucketHelper.BITBUCKET_API_ENDPOINTS['branch-permissions-projects'].format(
                    url=module.params['url'],
                    projectKey=project_key,
        )
    else:
        url = BitbucketHelper.BITBUCKET_API_ENDPOINTS['branch-permissions-repos'].format(
                    url=module.params['url'],
                    projectKey=project_key,
                    repositorySlug=repository,
        )

    info, content = bitbucket.request(
        api_url=url,
        method='POST',
        data={
            'type': restriction_type,
            'matcher': matcher,
            'users': users,
            'groups': groups,
            'accessKeys': accessKeys,
        },
    )

    if info['status'] == 200:
        return content

    if info['status'] == 400:
        module.fail_json(msg='The request has failed validation')

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to perform this operation.')

    if info['status'] != 200:
        module.fail_json(msg='Failed to create branch permissions in the supplied project and/or repository: {info}'.format(
            info=info,
        ))

    return None


def delete_branch_permission(module, bitbucket, project_key=None, repository=None, restriction_id=None):
    """
    Delete branch restrictions for the supplied project or repository.

    """

    if repository is None:
        url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['branch-permissions-projects'] + '/{id}').format(
                    url=module.params['url'],
                    projectKey=project_key,
                    id=restriction_id,
        )
    else:
        url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['branch-permissions-repos'] + '/{id}').format(
                    url=module.params['url'],
                    projectKey=project_key,
                    repositorySlug=repository,
                    id=restriction_id,
        )

    info, content = bitbucket.request(
        api_url=url,
        method='DELETE',
    )

    if info['status'] == 204:        
        return content        

    if info['status'] != 204:
        module.fail_json(msg='Failed to delete branch permissions in the supplied project and/or repository: {info}'.format(
            info=info,
        ))

    return None


def get_restriction_type(prevent=None):
    """
    Returns restiction type based on the supplied prevent name
    """  

    return {
        'deletion': 'no-deletes',
        'rewriting history': 'fast-forward-only',
        'changes without a pull request': 'pull-request-only',
        'all changes': 'read-only'
    }.get(prevent, 'unknown-restriction')


def get_matcher(matcher_type=None, matcher_name=None):
    """
    Create matcher dict based on the supplied matcher type and name
    """
    matcher = {}

    if matcher_type == 'branch_name':
        matcher = dict(
            active=True,
            displayId=matcher_name,
            id='refs/heads/' + matcher_name,
            type=dict(
                id="BRANCH",
                name="Branch"
            ),
        )

    if matcher_type == 'branch_pattern':
        matcher = dict(
            active=True,
            displayId=matcher_name,
            id=matcher_name,
            type=dict(
                id="PATTERN",
                name="Pattern"
            ),
        )

    if matcher_type == 'branching_model':
        if (matcher_name == 'development' or 'production'):
            matcher = dict(
                active=True,
                displayId=matcher_name.capitalize(),
                id=matcher_name,
                type=dict(
                    id="MODEL_BRANCH",
                    name="Branching model branch"
                ),
            )
        else:
            matcher = dict(
                active=True,
                displayId=matcher_name.capitalize(),
                id=matcher_name.upper(),
                type=dict(
                    id="MODEL_CATEGORY",
                    name="Branching model category"
                ),
            )

    return matcher
    

def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=False, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        branch_name=dict(type='str', required=False, no_log=False),
        branch_pattern=dict(type='str', required=False, no_log=False),
        branching_model=dict(type='str', choices=['feature', 'bugfix', 'hotfix', 'release', 'development', 'production'], required=False, no_log=False),
        restrictions=dict(
            type='list', 
            elements='dict', required=True, no_log=False,
            options=dict(
                prevent=dict(type='str', choices=['deletion', 'rewriting history', 'changes without a pull request', 'all changes'], required=True, no_log=False),
                exemptions=dict(
                    type='dict',
                    required=False, 
                    no_log=False,
                    default=dict(groups=list(), users=list(), access_keys=list()),
                    options=dict(
                        groups=dict(type='list', elements='str', required=False, no_log=False, default=list()),
                        users=dict(type='list', elements='str', required=False, no_log=False, default=list()),
                        access_keys=dict(type='list', elements='str', required=False, no_log=False, default=list()),
                    ),
                ),
            ),
        ),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token'), ('branch_name', 'branch_pattern', 'branching_model')],
        mutually_exclusive=[('username', 'token'), ('branch_name', 'branch_pattern', 'branching_model')],
        required_if=[('state', 'present', ('restrictions',), True)],
    )

    bitbucket = BitbucketHelper(module)

    state = module.params['state']
    project_key = module.params['project_key'] 
    repository = module.params['repository']
    return_content = module.params['return_content']
    branch_name = module.params['branch_name']
    branch_pattern = module.params['branch_pattern']
    branching_model = module.params['branching_model']
    restrictions = module.params['restrictions']
    scope_type = "PROJECT"

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=project_key,
        state=state,
        results=[],
        messages=[],
    )
    if repository is not None:
        result['repository'] = repository
        scope_type = "REPOSITORY"
    if branch_name is not None:
        result['branch_name'] = branch_name
        matcher = get_matcher(matcher_type='branch_name', matcher_name=branch_name)
    if branch_pattern is not None:
        result['branch_pattern'] = branch_pattern
        matcher = get_matcher(matcher_type='branch_pattern', matcher_name=branch_pattern)
    if branching_model is not None:
        result['branching_model'] = branching_model
        matcher = get_matcher(matcher_type='branching_model', matcher_name=branching_model)
    if restrictions is not None:
        result['restrictions'] = restrictions

    # Check if projects exist. Retrun message if it does not exist.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=project_key
        ))
        module.exit_json(**result)

    # When repository name is supplied but it does not exists, then return with a message.
    if (repository is not None) and (not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=project_key, repository=repository)):
        result['messages'].append('Repository `{repository}` does not exist.'.format(
            repository=repository
        ))
        module.exit_json(**result)

    # Retrieve existing branch permissions (restrictions) information (if any)
    existing_branch_permissions = bitbucket.get_branch_permissions_info(fail_when_not_exists=False, project_key=project_key, repository=repository)

    # Iterate over the supplied restictions
    for restriction in restrictions:        
        if restriction['exemptions'] is None:
            restriction['exemptions'] = dict(groups=list(), users=list(), access_keys=list())

        exemptions_groups = restriction['exemptions']['groups']
        exemptions_users = restriction['exemptions']['users']
        exemptions_access_keys = restriction['exemptions']['access_keys']        
        restriction_type = get_restriction_type(prevent=restriction['prevent'])        

        # Search for matching restrictions in existing branch permissions list
        found = [p for p in existing_branch_permissions if
                       p.get('matcher', {}) == matcher 
                   and p.get('type', 'no_type') == restriction_type
                   and [g.lower() for g in p.get('groups', [])] == [g.lower() for g in exemptions_groups]
                   and [u['name'] for u in p.get('users', [])] == [u.upper() for u in exemptions_users]
                   and p.get('accessKeys', []) == exemptions_access_keys
                   and p.get('scope', {}).get('type', 'no_type') == scope_type]

        # Check if restriction does not exist yet
        if not found:
            # Create the restriction if it does not exist and state == 'present'
            if state == 'present':
                if not module.check_mode:
                    result['results'].append(create_branch_permission(module, bitbucket, project_key=project_key, repository=repository, restriction_type=restriction_type,
                                                                      matcher=matcher, users=exemptions_users, groups=exemptions_groups, accessKeys=exemptions_access_keys))                         
                result['changed'] = True
        
        else:
            # Delete the restriction if it exists and state == 'absent'
            if state == 'absent':
                if not module.check_mode:
                    delete_result = delete_branch_permission(module, bitbucket, project_key=project_key, repository=repository, restriction_id=found[0].get('id', 'none'))
                    delete_result.update(restriction=found[0], status='deleted')
                    result['results'].append(delete_result)
                result['changed'] = True


    module.exit_json(**result)

if __name__ == '__main__':
    main()
