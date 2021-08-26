#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_project_reviewer
short_description: Manage default reviewer setting on project level
description:
- Configure default reviewers for project
- Only projects for which the authenticated user has the admin right can be managed.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Pawel Smolarz (pawel.smolarz@nordea.com)
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
  reviewers:
    description:
    - List of project default reviewers
    type: list
    required: true
  branch:
    description:
    - Branch name
    type: str
    default: master
    required: true
  approvals:
    description:
    - Number of approvals required 
    type: str
    default: 0
    required: false
notes:
- Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Configure default reviewer globally on AIMT project for master branch
  esp.bitbucket.bitbucket_project_reviewer:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    project_key: 'AIMT'
    validate_certs: no
    reviewers: [ user1 ]
    branch: 'master'
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


def add_default_reviewer(module, bitbucket):

    # Parse `reviewers` parameter and create list of reviewers.
    # It's possible someone passed a comma separated string, so we should handle that.
    reviewers = [p.strip() for p in module.params['reviewers']]
    reviewers = bitbucket.listify_comma_sep_strings_in_list(reviewers)
    if not reviewers:
        reviewers = []

    reviewers_data = []
    reviewers_data_json = []
    for r in reviewers:
        userid = bitbucket.get_users_id(r)
        reviewers_data.append({'user':r,'id': userid})

    for index in range(len(reviewers)):
        json_rev = {'id': reviewers_data[index].get('id')
                    # 'type': 'NORMAL',
                    # 'active': 'true'
                    }
        reviewers_data_json.append(json_rev)

    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['reviewers-project'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
        ),
        method='POST',
        data={
            'reviewers': reviewers_data_json,
            "sourceMatcher": {
                "active": 'true',
                "id": "refs/heads/**",
                "displayId": "refs/heads/**",
                "type": {
                    "id": "PATTERN",
                    "name": "Pattern"
                }
            },
            "targetMatcher": {
                "active": 'true',
                "id": "refs/heads/"+module.params['branch'],
                "displayId": module.params['branch'],
                "type": {
                    "id": "BRANCH",
                    "name": "Branch"
                }
            },
            "requiredApprovals": int(module.params['approvals'])
        },
    )

    if info['status'] == 200:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to manage `{project_key}` project.'.format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 404:
        module.fail_json(msg='Project `{project_key}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))

    if info['status'] == 409:
        module.fail_json(msg='Wrong reviewer provided.')

    if info['status'] == 400:
        module.fail_json(msg='Wrong body format: `{body}`'.format(body=reviewers_data_json))

    return None

def delete_default_reviewer(module, bitbucket, reviewid):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['reviewers-project-delete'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            id=reviewid
        ),
        method='DELETE',
    )

    if info['status'] == 204:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to write to `{project_key}` project.'.format(
            projectKey=module.params['project_key'],
        ))

    if info['status'] == 404:
        module.fail_json(msg='Project `{project_key}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))

    if info['status'] == 400:
        module.fail_json(msg='Wrong request.')

    return None

def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        branch=dict(type='str', default='master', required=False),
        approvals=dict(type='str', default='0', required=False),
        reviewers=dict(type='list', elements='str', no_log=False, default=list()),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')],
        required_if=[('state', 'present', ('reviewers','approvals'))],
    )

    bitbucket = BitbucketHelper(module)

    state = module.params['state']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        state=module.params['state'],
        messages=[],
        json={},
    )

    # Fail if number of approvals is higher than reviewers len
    if int(module.params['approvals']) > len(module.params['reviewers']) and state == 'present':
        result['messages'].append('Number of approvals required {} is higher than number of reviewers provided {}.'.format(
            module.params['approvals'],
            len(module.params['reviewers']),
        ))
        module.fail_json(msg=result['messages'])

    # Fail if number of reviewers is 0
    if len(module.params['reviewers']) == 0 and state == 'present':
        result['messages'].append('Please provide reviewers.')
        module.fail_json(msg=result['messages'])

    # Check if project and repository exist. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))
        module.fail_json(msg=result['messages'])

    # Retrieve existing reviewers information (if any)
    existing_reviewers = bitbucket.get_project_reviewers(fail_when_not_exists=False, filter=None)

    # Create new default reviewer in case it does not exist
    if state == 'present' and not any(
            d.get('targetRefMatcher', 'non_existing_reviewer_branch')['displayId'] == "refs/heads/" + module.params['branch'] for d in existing_reviewers):
        if not module.check_mode:
            result['json'] = add_default_reviewer(module, bitbucket)
        result['changed'] = True
    # Delete default project reviewer
    elif existing_reviewers and (state == 'absent'):
        for d in existing_reviewers:
            if d.get('targetRefMatcher', 'non_existing_reviewer_branch')['displayId'] == "refs/heads/" + module.params['branch']:
                if not module.check_mode:
                    result['json'] = delete_default_reviewer(module, bitbucket, d.get('id'))
                result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()