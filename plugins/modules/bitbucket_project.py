#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# Copyright: (c) 2019, Evgeniy Krysanov <evgeniy.krysanov@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_project
short_description: Manage your projects on Bitbucket Server
description:
- Manages Bitbucket Server projects.
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
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]
  name:
    description:
    - Bitbucket project name.
    - Required when I(state=present).
    type: str
    required: false
    aliases: [ project_name ]      
  description:
    description:
    - Bitbucket project description.
    - Required when I(state=present).
    type: str
    required: false
  avatar:
    description:
    - Bitbucket project custom avatar. Base64-encoded image data.
    type: str
    required: false    
  state:
    description:
    - Whether the project should exist or not.
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
- name: Create project
  esp.bitbucket.bitbucket_project:
    url: 'https://bitbucket.example.com'
    username: admin
    password: secrect
    project_key: FOO
    project_name: A new Bitbucket project
    description: |
        This is a new Bitbucket project.
    validate_certs: no
    state: present

- name: Create project with custom avatar using token
  esp.bitbucket.bitbucket_project:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    project_key: FOO
    name: A new Bitbucket project
    description: |
        This is a new Bitbucket project
    avatar: "{{ lookup('file', 'avatar.png', errors='ignore') | b64encode }}"
    validate_certs: no
    state: present

- name: Delete project
  esp.bitbucket.bitbucket_project:
    url: 'https://bitbucket.example.com'
    username: admin
    password: secrect
    project_key: FOO
    validate_certs: no
    state: absent
'''

RETURN = r'''
key:
    description: Bitbucket project key.
    returned: success
    type: str
    sample: FOO
name:
    description: Bitbucket project name (if I(state=present)).
    returned: success
    type: str
    sample: A new Bitbucket project
description:
    description: Bitbucket project description (if I(state=present)).
    returned: success
    type: str
    sample: This is a new Bitbucket project
public:
    description: Whether or not the project is public (if I(state=present)).
    returned: success
    type: bool
    sample: false
type:
    description: Bitbucket project type (if I(state=present)).
    returned: success
    type: str
    sample: NORMAL
id:
    description: Project ID (if I(state=present)).
    returned: success
    type: int
    sample: 200 
links:
    description: Links to Bitbucket project (if I(state=present)).
    returned: success
    type: dict
    contains:
        self:
            description: Links to Bitbucket repository.
            returned: success
            type: list
            elements: dict
            sample:
                - href: https://bitbucket.example.com/projects/FOO  
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper

error_messages = {
    'required_project_name': '`name` is required when the `state` is `present`',
    'required_description': '`description` is required when the `state` is `present`',
    'insufficient_permissions_to_see': 'The currently authenticated user has insufficient permissions to view `{projectKey}` project',
    'project_does_not_exist': '`{projectKey}` project does not exist.',
    'validation_error': '`{projectKey}` project was not created due to a validation error',
    'project_already_exists': 'The project key ({projectKey}) or name ({name}) is already in use',
    'project_contains_repositories': '`{projectKey}` project can not be deleted as it contains repositories',
    'insufficient_permissions_to_delete': 'The currently authenticated user has insufficient permissions to delete `{projectKey}` project',
    'insufficient_permissions_to_create': 'The currently authenticated user has insufficient permissions to create `{projectKey}` project',
}


def create_project(module, bitbucket):
    data = {
        'key': module.params['project_key'],
        'name': module.params['name'],
        'description': module.params['description'],
    }

    if module.params['avatar'] is not None:
        data.update({
            'avatar': 'data:image/png;base64,{0}'.format(module.params['avatar']),
        })

    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['projects'].format(
            url=module.params['url'],
        ),
        method='POST',
        data=data,
    )

    if info['status'] == 201:
        return content

    if info['status'] == 400:
        module.fail_json(msg=error_messages['validation_error'].format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 401:
        module.fail_json(msg=error_messages['insufficient_permissions_to_create'].format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 409:
        module.fail_json(msg=error_messages['project_already_exists'].format(
            projectKey=module.params['project_key'],
            name=module.params['name'],
        ))

    if info['status'] != 201:
        module.fail_json(msg='Failed to create project with the supplied projectKey `{projectKey}`: {info}'.format(
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def delete_project(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['projects-projectKey'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
        ),
        method='DELETE',
    )

    if info['status'] == 204:
        return content

    if info['status'] == 401:
        module.fail_json(msg=error_messages['insufficient_permissions_to_delete'].format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 404:
        module.fail_json(msg=error_messages['project_does_not_exist'].format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 409:
        module.fail_json(msg=error_messages['project_contains_repositories'].format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] != 204:
        module.fail_json(msg='Failed to delete project `{projectKey}`: {info}'.format(           
            projectKey=module.params['project_key'],
            info=info,
        ))

    return None


def check_arguments(module):
    if (module.params['name'] is None) and (module.params['state'] == 'present'):
        module.fail_json(msg=error_messages['required_project_name'])

    if (module.params['description'] is None) and (module.params['state'] == 'present'):
        module.fail_json(msg=error_messages['required_description'])


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        name=dict(type='str', required=False, no_log=False, aliases=['project_name']),
        description=dict(type='str', required=False, no_log=False),
        avatar=dict(type='str', required=False, no_log=False),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password'),('name', 'description')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    state = module.params['state']
    return_content = module.params['return_content']

    # Check arguments
    check_arguments(module)

    # Retrieve existing project information (if any)
    content = existing_project = bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key'])
    changed = False

    # Create new project in case it doesn't exists
    if not existing_project and (state == 'present'):
        if not module.check_mode:
            content = create_project(module, bitbucket)
        changed = True

    # Delete project
    elif existing_project and (state == 'absent'):
       if not module.check_mode:
           content = delete_project(module, bitbucket)
       changed = True

    if content is not None:
        module.exit_json(changed=changed, **content)
    else:
        module.exit_json(changed=changed)


if __name__ == '__main__':
    main()