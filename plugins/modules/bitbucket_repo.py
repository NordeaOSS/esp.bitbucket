#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# Copyright: (c) 2019, Evgeniy Krysanov <evgeniy.krysanov@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_repo
short_description: Manage your repositories on Bitbucket Server
description:
- Manages Bitbucket Server repositories.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
  - Evgeniy Krysanov (@catcombo)
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
  state:
    description:
    - Whether the repository should exist or not.
    type: str
    default: present
    choices: [ absent, present ]
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
- name: Create repository
  esp.bitbucket.bitbucket_repo:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: present

- name: Create repository using token
  esp.bitbucket.bitbucket_repo:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    name: bar
    project: FOO
    validate_certs: no
    state: present

- name: Delete repository
  esp.bitbucket.bitbucket_repo:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: absent
'''

RETURN = r'''
name:
    description: Bitbucket repository name (if I(state=present)).
    returned: success
    type: str
    sample: bar
project:
    description: Information about Bitbucket project (if I(state=present)).
    returned: success
    type: dict
    contains:
        id:
            description: Project ID.
            returned: success
            type: int
            sample: 200
        key:
            description: Bitbucket project key.
            returned: success
            type: str
            sample: FOO
        name:
            description: Bitbucket project name.
            returned: success
            type: str
            sample: FOO project
        public:
            description: Whether or not the project is public.
            returned: success
            type: bool
            sample: false
        type:
            description: Bitbucket project type.
            returned: success
            type: str
            sample: NORMAL
        self:
            description: Links to Bitbucket project.
            returned: success
            type: list
            elements: dict
            sample:
                - href: https://bitbucket.example.com/projects/FOO  
links:
    description: Links to Bitbucket repository (if I(state=present)).
    returned: success
    type: dict
    contains:
        clone:
            description: Clone URLs.
            returned: success
            type: list
            elements: dict
            sample:
                - href: https://bitbucket.example.com/scm/foo/bar.git  
                  name: http
                - href: ssh://git@bitbucket.example.com:7999/foo/bar.git  
                  name: ssh
        self:
            description: Links to Bitbucket repository.
            returned: success
            type: list
            elements: dict
            sample:
                - href: https://bitbucket.example.com/projects/FOO/repos/bar/browse   
forkable:
    description: Source file used for the copy on the target machine (if I(state=present)).
    returned: success
    type: bool
    sample: true
hierarchyId:
    description: Hierarchy ID (if I(state=present)).
    returned: success
    type: str
    sample: 91369a5b9598e936d126
id:
    description: Repository ID (if I(state=present)).
    returned: success
    type: int
    sample: 100
public:
    description: Whether or not the repository is public (if I(state=present)).
    returned: success
    type: bool
    sample: true
scmId:
    description: SCM type (if I(state=present)).
    returned: success
    type: str
    sample: git
slug:
    description: Bitbucket repository slug name (if I(state=present)).
    returned: success
    type: str
    sample: bar
state:
    description: Bitbucket repository state, after execution (if I(state=present)).
    returned: success
    type: str
    sample: AVAILABLE
statusMessage:
    description: Bitbucket repository state message, after execution (if I(state=present)).
    returned: success
    type: str
    sample: Available
context:
    description: Context (if I(state=absent)).
    returned: success
    type: str
    sample: null
exceptionName:
    description: Exception Name (if I(state=absent)).
    returned: success
    type: str
    sample: null
message:
    description: Deletion message (if I(state=absent)).
    returned: success
    type: str
    sample: Repository scheduled for deletion.
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


error_messages = {
    'insufficient_permissions_to_see': 'The currently authenticated user has insufficient permissions to see `{repositorySlug}` repository',
    'repository_does_not_exist': '`{repositorySlug}` repository does not exist',
    'validation_error': '`{repositorySlug}` repository was not created due to a validation error',
    'repository_already_exists': 'A repository with same name ({repositorySlug}) already exists',
    'insufficient_permissions_to_delete': 'The currently authenticated user has insufficient permissions to delete `{repositorySlug}` repository',
    'insufficient_permissions_to_create': 'The currently authenticated user has insufficient permissions to create `{repositorySlug}` repository',
}


def create_repository(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['repos'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
        ),
        method='POST',
        data={
            'name': module.params['repository'],
        },
    )

    if info['status'] == 201:
        return content

    if info['status'] == 400:
        module.fail_json(msg=error_messages['validation_error'].format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 401:
        module.fail_json(msg=error_messages['insufficient_permissions_to_create'].format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 409:
        module.fail_json(msg=error_messages['repository_already_exists'].format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] != 201:
        module.fail_json(msg='Failed to create repository `{repositorySlug}` in the supplied projectKey `{projectKey}`: {info}'.format(
            repositorySlug=module.params['repository'],            
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def delete_repository(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['repos-repositorySlug'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
        ),
        method='DELETE',
    )

    if info['status'] == 202:
        return content

    if info['status'] == 204:
        module.fail_json(msg=error_messages['repository_does_not_exist'].format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 401:
        module.fail_json(msg=error_messages['insufficient_permissions_to_delete'].format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] != 202:
        module.fail_json(msg='Failed to delete repository `{repositorySlug}` in the supplied projectKey `{projectKey}`: {info}'.format(
            repositorySlug=module.params['repository'],            
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False, aliases=['name']),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
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
    return_content = module.params['return_content']

    # Retrieve existing repository information (if any)
    content = existing_repository = bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=module.params['repository'])
    changed = False

    # Create new repository in case it doesn't exist
    if not existing_repository and (state == 'present'):
        if not module.check_mode:
            content = create_repository(module, bitbucket)
        changed = True

    # Delete repository
    elif existing_repository and (state == 'absent'):
       if not module.check_mode:
           content = delete_repository(module, bitbucket)
       changed = True

    if content is not None:
        module.exit_json(changed=changed, **content)
    else:
        module.exit_json(changed=changed)

if __name__ == '__main__':
    main()