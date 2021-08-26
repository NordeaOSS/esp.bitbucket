#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_project_permissions_info
short_description: Retrieve Bitbucket project permissions information
description:
- Retrieve a list of groups and users that have been granted at least one permission for the specified project.
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
  filters:
    description:
    - If specified, only group or user names containing the supplied filter strings will be returned.
    - This can be '*' which means all groups and users.
    - Filters are concatenated with OR operator.
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
- name: Retrieve Bitbucket project permissions information
  esp.bitbucket.bitbucket_project_permissions_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: FOO
    validate_certs: no

- name: Retrieve Bitbucket project permissions, only group or user names containing the supplied filter strings will be returned
  esp.bitbucket.bitbucket_project_permissions_info:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    project_key: FOO
    filters: [ admin, read ]
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
groups:
    description: List of Bitbucket groups that have been granted at least one permission for the specified project.
    returned: always
    type: list
    elements: dict
    contains:
        group:
            description: Bitbucket group details.
            returned: success
            type: dict
            contains:
                name:
                    description: Bitbucket group name.
                    returned: success
                    type: str
                    sample: group-read
        permission:
            description: Bitbucket permission name.
            returned: success
            type: str
            sample: PROJECT_READ
users:
    description: List of Bitbucket users that have been granted at least one permission for the specified project.
    returned: always
    type: list
    elements: dict
    contains:
        user:
            description: Bitbucket user details.
            returned: success
            type: dict
            contains:
                name:
                    description: Bitbucket user name.
                    returned: success
                    type: str
                    sample: admin
                type:
                    description: Bitbucket user type.
                    returned: success
                    type: str
                    sample: NORMAL
                slug:
                    description: Bitbucket user slug.
                    returned: success
                    type: str
                    sample: admin      
                active:
                    description: Bitbucket user active status.
                    returned: success
                    type: bool
                    sample: true     
                displayName:
                    description: Bitbucket user displayName.
                    returned: success
                    type: str
                    sample: admin    
                id:
                    description: Bitbucket user id.
                    returned: success
                    type: int
                    sample: 9000                   
        permission:
            description: Bitbucket permission name.
            returned: success
            type: str
            sample: PROJECT_ADMIN
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        filters=dict(type='list', elements='str', no_log=False, default=[ '*' ]),
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

    # Parse `filters` parameter and create list of filters.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '*' which means all projects.
    filters = []
    filters = [p.strip() for p in module.params['filters']]
    filters = bitbucket.listify_comma_sep_strings_in_list(filters)
    if not filters:
        filters = [ '*' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        filters=module.params['filters'],
        project_key=project_key,
        users=[],
        groups=[],
        messages=[],
    )

    # Check if projects exist. Retrun message if it does not exist.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=project_key
        ))
    else:
        # Retrieve permissions information
        if '*' in filters:
            result['groups'].extend( bitbucket.get_project_permissions_info(fail_when_not_exists=False, project_key=project_key, scope='groups', filter=None) )
            result['users'].extend( bitbucket.get_project_permissions_info(fail_when_not_exists=False, project_key=project_key, scope='users', filter=None) )
        else:    
            for filter in filters:
                result['groups'].extend( bitbucket.get_project_permissions_info(fail_when_not_exists=False, project_key=project_key, scope='groups', filter=filter) )
                result['users'].extend( bitbucket.get_project_permissions_info(fail_when_not_exists=False, project_key=project_key, scope='users', filter=filter) )

    module.exit_json(**result)


if __name__ == '__main__':
    main()