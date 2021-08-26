#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_repo_permissions
short_description: Manage Bitbucket repository permissions
description:
- Promote or demote a group's or a users's permission level for the specified repository.
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
    required: true
    aliases: [ name ]     
  user:
    description:
    - Bitbucket user to grant or revoke permission from.
    - This is only needed when not using I(group).
    type: str
    required: false
  group:
    description:
    - Bitbucket group to grant or revoke permission from.
    - This is only needed when not using I(user).
    type: str
    required: false  
  permission:
    description:
    - The permission to grant.
    - Empty string '' means revoke all grants form a user or group.
    type: str
    choices: [ REPO_READ, REPO_WRITE, REPO_ADMIN, '' ]
    required: true
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
- name: Set REPO_WRITE permission level for the specified repository to jsmith user
  esp.bitbucket.bitbucket_repo_permissions:
    url: 'https://bitbucket.example.com'
    username: admin
    password: secrect
    project_key: FOO
    repository: bar
    user: jsmith
    permission: REPO_WRITE
    validate_certs: no

- name: Revoke all permissions for the specified repository from a group
  esp.bitbucket.bitbucket_repo_permissions:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    project_key: FOO
    repository: bar
    group: dev-group
    permission: ''
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
permission:
    description: The permission to grant. Empty string '' means revoke all grants form a user or group.
    returned: always
    type: str
    sample: REPO_WRITE
user:
    description: Bitbucket user to grant or revoke permission from.
    returned: success
    type: str
    sample: jsmith
group:
    description: Bitbucket group to grant or revoke permission from.
    returned: success
    type: str
    sample: dev-group
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def grant_repository_permissions(module, bitbucket, fail_when_not_exists=False, project_key=None, repository=None, scope=None, name=None, permission=None):
    """
    Promote or demote either a user's or a group's permission level for the specified repository
    scope: either 'users' or 'groups'.

    when fail_when_not_exists=False it just returns None and does not fail
    """
    info, content = bitbucket.request(
        api_url=(bitbucket.BITBUCKET_API_ENDPOINTS['repos-permissions'] + '/{scope}?name={name}&permission={permission}').format(
            url=module.params['url'],
            projectKey=project_key,
            repositorySlug=repository,
            scope=scope,
            name=name,
            permission=permission,
        ),
        method='PUT',
    )              

    if info['status'] == 204:
        return content

    if info['status'] == 400:
        module.fail_json(msg='The request was malformed or the specified permission ({permission}) does not exist.'.format(
            permission=permission,
        ))

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user is not a repository administrator for {repositorySlug} repository.'.format(
            repositorySlug=repository,
        ))

    if info['status'] == 403:
        module.fail_json(msg='The action was disallowed as it would reduce the currently authenticated user permission level.')

    if info['status'] == 404:
        if fail_when_not_exists:
            module.fail_json(msg='The specified repository or user or group does not exist')
        else:
            return None

    if info['status'] != 204:
        self.module.fail_json(msg='Failed to grant permission data which matches the supplied projectKey `{projectKey}`, `{repositorySlug}` repository, `{name}` object and `{permission}` permission: {info}'.format(
            projectKey=project_key,
            repositorySlug=repository,
            name=name,
            permission=permission,
            info=info,
        ))

    return None


def revoke_repository_permissions(module, bitbucket, fail_when_not_exists=False, project_key=None, repository=None, scope=None, name=None):
    """
    Revoke all permissions for the specified repository for a user or a group.
    scope: either 'users' or 'groups'.

    when fail_when_not_exists=False it just returns None and does not fail
    """
    info, content = bitbucket.request(
        api_url=(bitbucket.BITBUCKET_API_ENDPOINTS['repos-permissions'] + '/{scope}?name={name}').format(
            url=module.params['url'],
            projectKey=project_key,
            repositorySlug=repository,
            scope=scope,
            name=name,
        ),
        method='DELETE',
    )              

    if info['status'] == 204:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user is not a repository administrator for {repositorySlug} repository.'.format(
            repositorySlug=repository,
        ))

    if info['status'] == 404:
        if fail_when_not_exists:
            module.fail_json(msg='The specified repository or user or group does not exist')
        else:
            return None

    if info['status'] == 409:
        module.fail_json(msg='The action was disallowed as it would reduce the currently authenticated user permission level.')

    if info['status'] != 204:
        self.module.fail_json(msg='Failed to revoke permissions which matches the supplied projectKey `{projectKey}`, `{repositorySlug}` repository, `{name}` object: {info}'.format(
            projectKey=project_key,
            repositorySlug=repository,
            name=name,
            info=info,
        ))

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False, aliases=['name']),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        permission=dict(type='str', no_log=False, choices=['REPO_READ', 'REPO_WRITE', 'REPO_ADMIN', '' ]),
        user=dict(type='str', no_log=False, required=False, default=None),
        group=dict(type='str', no_log=False, required=False, default=None),
        username=dict(type='str', no_log=False, required=False, default=None, fallback=(env_fallback, ['BITBUCKET_USER_ID'])),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token'), ('user', 'group')],
        mutually_exclusive=[('username', 'token'), ('user', 'group')]
    )

    bitbucket = BitbucketHelper(module)

    module.params['return_content'] = True

    project_key = module.params['project_key']
    repository = module.params['repository']     

    # Seed the result dict in the object
    result = dict(
        changed=False,
        permission=module.params['permission'],
        project_key=project_key,
        repository=repository,
        json={},
        messages=[],
    )
    if module.params['user'] is not None:
        result['user'] = module.params['user']
    if module.params['group'] is not None:
        result['group'] = module.params['group']

    # Check if projects exist. Retrun message if it does not exist.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=project_key
        ))
    else:
        # Check if repository exist. Retrun message if it does not exist.
        if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=project_key, repository=repository):
            result['messages'].append('Repository `{repository}` does not exist.'.format(
                repository=repository
            ))
        else:
            # If user is specified..
            if module.params['user'] is not None:
                # Get a list of users that have been granted at least one permission for the specified repository.
                users_with_access = bitbucket.get_repository_permissions_info(fail_when_not_exists=False, project_key=project_key, repository=repository, scope='users', filter=None)

                # When the user is on the list and their grants should be revoked..
                if (module.params['permission'] == '') and (any(user['user']['name'].lower() == module.params['user'].lower() for user in users_with_access)):
                    if not module.check_mode:
                        result['json'] = revoke_repository_permissions(module=module, bitbucket=bitbucket, fail_when_not_exists=True, 
                                                                       project_key=project_key, repository=repository, scope='users', name=module.params['user'])
                    result['changed'] = True

                # When either the user is NOT on the list or the user is on the list and their grants should be changed (promoted or demoted)..
                if (module.params['permission'] != '') and (not any(user['user']['name'].lower() == module.params['user'].lower() and user['permission'].upper() == module.params['permission'].upper() for user in users_with_access)):
                    if not module.check_mode:
                        result['json'] = grant_repository_permissions(module=module, bitbucket=bitbucket, fail_when_not_exists=True, 
                                                                      project_key=project_key, repository=repository, scope='users', name=module.params['user'], 
                                                                      permission=module.params['permission'])
                    result['changed'] = True

            # If group is specified..
            if module.params['group'] is not None:
                # Get a list of groups that have been granted at least one permission for the specified repository.
                groups_with_access = bitbucket.get_repository_permissions_info(fail_when_not_exists=False, project_key=project_key, repository=repository, scope='groups', filter=None)

                # When the group is on the list and their grants should be revoked..
                if (module.params['permission'] == '') and (any(group['group']['name'].lower() == module.params['group'].lower() for group in groups_with_access)):
                    if not module.check_mode:
                        result['json'] = revoke_repository_permissions(module=module, bitbucket=bitbucket, fail_when_not_exists=True, 
                                                                       project_key=project_key, repository=repository, scope='groups', name=module.params['group'])
                    result['changed'] = True

                # When either the group is NOT on the list or the group is on the list and their grants should be changed (promoted or demoted)..
                if (module.params['permission'] != '') and (not any(group['group']['name'].lower() == module.params['group'].lower() and group['permission'].upper() == module.params['permission'].upper() for group in groups_with_access)):
                    if not module.check_mode:
                        result['json'] = grant_repository_permissions(module=module, bitbucket=bitbucket, fail_when_not_exists=True, 
                                                                      project_key=project_key, repository=repository, scope='groups', name=module.params['group'], 
                                                                      permission=module.params['permission'])
                    result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()