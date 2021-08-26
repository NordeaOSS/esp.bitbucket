#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_project_info
short_description: Retrieve project information
description:
- Retrieve project information from Bitbucket Server for the supplied project key filter.
- Only projects for which the authenticated user has the PROJECT_VIEW permission will be returned.
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
  project_key:
    description:
    - Retrieve projects matching the supplied I(project_key) filter.
    - This can be '*' which means all projects.
    type: list
    required: false
    default: [ '*' ]
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
- Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Retrieve all projects
  esp.bitbucket.bitbucket_project_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: [ '*' ]
    validate_certs: no

- name: Retrieve the projects matching the supplied project_key filter
  esp.bitbucket.bitbucket_project_info:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    project_key: [ FOO, BAR ]
    validate_certs: no
'''

RETURN = r'''
messages:
    description: List of error messages.
    returned: always
    type: list
    sample:
      - Repository `bar2` does not exist. 
projects:
    description: List of Bitbucket projects.
    returned: always
    type: list
    contains:
        key:
            description: Bitbucket project key.
            returned: success
            type: str
            sample: FOO
        name:
            description: Bitbucket project name.
            returned: success
            type: str
            sample: A new Bitbucket project
        description:
            description: Bitbucket project description.
            returned: success
            type: str
            sample: This is a new Bitbucket project
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
        id:
            description: Project ID.
            returned: success
            type: int
            sample: 200 
        links:
            description: Links to Bitbucket project.
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


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        project_key=dict(type='list', elements='str', no_log=False, default=[ '*' ], aliases=['project']),
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

    # Parse `project_key` parameter and create list of projects.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '*' which means all projects.
    project_keys = []
    project_keys = [p.strip() for p in module.params['project_key']]
    project_keys = bitbucket.listify_comma_sep_strings_in_list(project_keys)
    if not project_keys:
        project_keys = [ '*' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        filter=project_keys,
        messages=[],
        projects=[],
    )

    # Retrieve project information
    if '*' in project_keys:
        result['projects'] = bitbucket.get_all_projects_info(fail_when_not_exists=False)
    else:    
        for project_key in project_keys:
            # Check if projects exist. Retrun message if it does not exist.
            project_response = bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key)
            if not project_response:
                result['messages'].append('Project `{projectKey}` does not exist.'.format(
                    projectKey=project_key
                ))
            else:
                result['projects'].append(project_response)

    module.exit_json(**result)


if __name__ == '__main__':
    main()