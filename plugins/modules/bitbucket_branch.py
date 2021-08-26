#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_branch
short_description: Manage repository branches on Bitbucket Server
description:
- Manages repository branches on Bitbucket Server.
- It creates a new branch, or sets an existing branch as a default for the supplied repository.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
  - Pawel Smolarz
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
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]  
  branch:
    description:
    - Branch name to create or delete
    type: str
    required: true
    aliases: [ name ]    
  from_branch:
    description:
    - New branch will be created from this branch.
    - Required when I(state=present).
    type: str
    default: master
    required: false    
  state:
    description:
    - Whether the branch should exist or not. Only creation allowed
    type: str
    default: present
    choices: [ present ]
    required: false
  is_default:
    description:
    - Set the new branch as default one for the repository.
    type: bool
    default: False
    required: false
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
- name: Create branch and set it as default one for the supplied repository
  esp.bitbucket.bitbucket_branch:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: present
    branch: feature/baz
    from_branch: master
    is_default: True
    
- name: Create branch
  esp.bitbucket.bitbucket_branch:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: present
    branch: feature/baz
    from_branch: master

- name: Update the default branch of a repository
  esp.bitbucket.bitbucket_branch:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    branch: develop
    is_default: True
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
    description: A specific branch name.
    returned: always
    type: str
    sample: develop  
from_branch:
    description: A source branch name which a new branch is created from.
    returned: success
    type: str
    sample: master    
state:
    description: Branch state, either I(present) or I(absent).
    returned: success
    type: str
    sample: present
is_default:
    description: Whether or not the branch is set as the default one.
    returned: success
    type: boolean
    sample: False
json:
    description: Details of a new branch.
    returned: success
    type: dict
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


def create_branch(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['branches'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
        ),
        method='POST',
        data={
            'name': module.params['branch'],
            'startPoint': "refs/heads/" + module.params['from_branch'],
        },
    )

    if info['status'] == 200:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to write to `{repositorySlug}` repository'.format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 404:
        module.fail_json(msg='Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=repository
        ))

    if info['status'] != 200:
        module.fail_json(msg='Failed to create `{branch}` branch in the supplied `{repositorySlug}` repository and `{projectKey}` project: {info}'.format(
            branch=module.params['branch'],
            repositorySlug=module.params['repository'],
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def delete_branch(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['branches'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
        ),
        method='DELETE',
        data={
            'name': "refs/heads/"+module.params['branch'],
            "dryRun": "false",
        },
    )

    if info['status'] == 202:
        return content

    # if info['status'] == 204:
    #     module.fail_json(msg=error_messages['repository_does_not_exist'].format(
    #         repositorySlug=module.params['repository'],
    #         project=module.params['project_key'],
    #         branch=module.params['from_branch'],
    #     ))

    # if info['status'] == 401:
    #     module.fail_json(msg=error_messages['insufficient_permissions_to_delete'].format(
    #         repositorySlug=module.params['repository'],
    #     ))

    if info['status'] != 202:
        module.fail_json(msg='Failed to delete branch `branch` in `{repositorySlug}` in the supplied projectKey `{projectKey}`: {info}'.format(
            branch=module.params['branch'],
            repositorySlug=module.params['repository'],
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present'], default='present'),
        branch=dict(type='str', required=True, aliases=['name']),
        from_branch=dict(type='str', default='master'),
        is_default=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    state = module.params['state']
    branch = module.params['branch']
    return_content = module.params['return_content']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        repository=module.params['repository'],
        state=module.params['state'],
        branch=module.params['branch'],
        from_branch=module.params['from_branch'],
        is_default=module.params['is_default'],
        json={},
    )

    # Retrieve existing branches information (if any)
    existing_branches = bitbucket.get_branches_info(fail_when_not_exists=False, filter=None)

    # Create new branch in case it does not exist
    if (state == 'present') and (not any(d.get('displayId', 'non_existing_branch') == branch for d in existing_branches)):
        if not module.check_mode:
            result['json'] = create_branch(module, bitbucket)
            if module.params['is_default']:
                bitbucket.set_default_branch(branch=branch)
        result['changed'] = True

    # Update non-default branch of a repository to the defaule one, when it exists and is_default parameter is set to True
    if (state == 'present') and (any(d.get('displayId', 'non_existing_branch') == branch and (not d.get('isDefault', False)) for d in existing_branches)) and (module.params['is_default']):
        if not module.check_mode:
            bitbucket.set_default_branch(branch=branch)
        result['changed'] = True

    # Delete branch when it exists
    # if (state == 'absent') and (any(d.get('displayId', 'non_existing_branch') == branch for d in existing_branches)):
    #     if not module.check_mode:
    #         result['json'] = delete_branch(module, bitbucket)
    #     result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()