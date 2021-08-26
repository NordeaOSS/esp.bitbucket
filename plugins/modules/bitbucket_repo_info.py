#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_repo_info
short_description: Retrieve repositories information for the supplied project
description:
- Retrieve repositories information from Bitbucket Server for the supplied project.
- Only repositories for which the authenticated user has the REPO_READ permission will be returned.
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
    - Retrieve repositories matching the supplied I(repository) filter.
    - This can be '*' which means all repositories.
    type: list
    required: false
    default: [ '*' ]
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
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
- name: Retrieve all repositories
  esp.bitbucket.bitbucket_repo_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: [ '*' ]
    project_key: FOO
    validate_certs: no

- name: Retrieve the repositories matching the supplied repository filter
  esp.bitbucket.bitbucket_repo_info:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    repository: [ bar, baz ]
    project_key: FOO
    validate_certs: no
'''

RETURN = r'''
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
      - Repository `baz` does not exist. 
repositories:
    description: List of repositories.
    returned: always
    type: list
    contains:
        forkable:
            description: Source file used for the copy on the target machine.
            returned: success
            type: bool
            sample: true
        hierarchyId:
            description: Hierarchy ID.
            returned: success
            type: str
            sample: 91369a5b9598e936d126
        id:
            description: Repository ID.
            returned: success
            type: int
            sample: 100
        public:
            description: Whether or not the repository is public.
            returned: success
            type: bool
            sample: true
        scmId:
            description: SCM type.
            returned: success
            type: str
            sample: git
        slug:
            description: Bitbucket repository slug name.
            returned: success
            type: str
            sample: bar
        name:
            description: Bitbucket repository name.
            returned: success
            type: str
            sample: bar            
        state:
            description: Bitbucket repository state, after execution.
            returned: success
            type: str
            sample: AVAILABLE
        statusMessage:
            description: Bitbucket repository state message, after execution.
            returned: success
            type: str
            sample: Available    
        links:
            description: Links to Bitbucket repository.
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
        project:
            description: Information about Bitbucket project.
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
                description:
                    description: Bitbucket project description.
                    returned: success
                    type: str
                    sample: This is a Bitbucket project                   
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
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),        
        repository=dict(type='list', elements='str', no_log=False, default=[ '*' ]),
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

    # Parse `repository` parameter and create list of repositories.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '*' which means all repositories.
    repositories = []
    repositories = [p.strip() for p in module.params['repository']]
    repositories = bitbucket.listify_comma_sep_strings_in_list(repositories)
    if not repositories:
        repositories = [ '*' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        filter=repositories,
        messages=[],
        repositories=[],
    )

    # Check if the project exists. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))

    # Retrieve repositories information if the project exists
    if not result['messages']:
        if '*' in repositories:
            result['repositories'] = bitbucket.get_all_repositories_info(fail_when_not_exists=False)
        else:
            for repository in repositories:
                # Check if the repository exists. Retrun message if it does not exist.
                repo_response = bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=repository)
                if not repo_response:
                    result['messages'].append('Repository `{repositorySlug}` does not exist.'.format(
                        repositorySlug=repository
                    ))
                else:                
                  result['repositories'].append(repo_response)

    module.exit_json(**result)


if __name__ == '__main__':
    main()