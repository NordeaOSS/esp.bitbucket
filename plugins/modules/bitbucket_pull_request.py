#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_pull_request
short_description: Manage repository pull requests on Bitbucket Server
description:
- Manages repository pull requests on Bitbucket Server.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Pawel Smolarz
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
    required: true
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]
  title:
    description:
    - Title for pull request
    type: str
    required: false
  from_branch:
    description:
    - Source branch for pull request
    type: str
    default: develop
    required: true
  to_branch:
    description:
    - Destination branch for pull request
    type: str
    default: master
    required: true
  reviewers:
    description:
    - List of pull request reviewers
    type: list
    required: false
  state:
    description:
    - Whether the pull should exist or not.
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
- name: Create pull request
  esp.bitbucket.bitbucket_pull_request:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: present
    title: "Pull request from develop to master branch"
    from_branch: "develop"
    to_branch: "master"
    reviewers: [ m00001, m00002 ]
    
- name: Delete pull request on repository
  esp.bitbucket.bitbucket_pull_request:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: absent
    from_branch: "develop"
    to_branch: "master"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def create_pull_request(module, bitbucket):

    # Parse `reviewers` parameter and create list of reviewers.
    # It's possible someone passed a comma separated string, so we should handle that.
    reviewers = []
    reviewers = [p.strip() for p in module.params['reviewers']]
    reviewers = bitbucket.listify_comma_sep_strings_in_list(reviewers)
    if not reviewers:
        reviewers = []

    reviewers_data = []
    for r in reviewers:
        json_rev = {'user': {'name': r.upper() }}
        reviewers_data.append(json_rev)

    # reviewers_data = []
    # for r in module.params['reviewers'].split(','):
    #     json_rev = {'user': {'name': r.upper() }}
    #     reviewers_data.append(json_rev)

    # msg.append(reviewers_data)

    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['pulls'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
        ),
        method='POST',
        data={
            'title': module.params['title'],
            'description':  module.params['title'],
            'state': 'open',
            'open': 'true',
            'closed': 'false',
            'fromRef': {
                'id': 'refs/heads/' + module.params['from_branch'],
                'repository': {
                    'slug': module.params['repository'],
                    'name': 'null',
                    'project': {
                        'key': module.params['project_key']
                    }
                }
            },
            'toRef': {
                'id': 'refs/heads/' + module.params['to_branch'],
                'repository': {
                    'slug': module.params['repository'],
                    'name': 'null',
                    'project': {
                        'key': module.params['project_key']
                    }
                }
            },
            'locked': 'false',
            'reviewers': reviewers_data
        },
    )

    if info['status'] == 201:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to write to `{repositorySlug}` repository'.format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 404:
        module.fail_json(msg='Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=repository
        ))

    if info['status'] == 409:
        module.fail_json(msg='Wrong reviewer provided.')


    return None

def delete_pull_request(module, bitbucket,pull_id,version):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['pulls-delete'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            pullid=pull_id,
        ),
        method='DELETE',
        data={
            'version': version,
        },
    )

    if info['status'] == 204:
        return content

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to write to `{repositorySlug}` repository'.format(
            repositorySlug=module.params['repository'],
        ))

    if info['status'] == 404:
        module.fail_json(msg='Pull `{pullid}` does not exist.'.format(
            pullid=module.params['pull_id']
        ))

    if info['status'] == 409:
        module.fail_json(msg='You are attempting to modify a pull request based on out-of-date information. Wrong version provided.')

    return None

def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        title=dict(type='str', default=''),
        from_branch=dict(type='str', default='develop'),
        to_branch=dict(type='str', default='master'),
        reviewers=dict(type='list', elements='str', no_log=False, default=list()),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password'), ('from_branch', 'to_branch')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')],
        required_if=[('state', 'present', ('title', 'reviewers'))],
    )

    bitbucket = BitbucketHelper(module)

    state = module.params['state']

    return_content = module.params['return_content']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        repository=module.params['repository'],
        state=module.params['state'],
        messages=[],
        json={},
    )

    # Check if project and repository exist. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        ))
        module.fail_json(msg=result['messages'])
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=module.params['repository']):
        result['messages'].append('Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=module.params['repository']
        ))
        module.fail_json(msg=result['messages'])

    # Retrieve existing pulls information (if any)
    existing_pulls = bitbucket.get_pull_request_info(fail_when_not_exists=False, filter=None)

    # Create new pull in case it does not exist
    if (state == 'present') and (
            (not any(d.get('fromRef', 'non_existing_pull_from_branch')['displayId'] == module.params['from_branch'] for d in existing_pulls))
            or
            (not any(d.get('toRef', 'non_existing_pull_to_branch')['displayId'] == module.params['to_branch'] for d in existing_pulls))
        ):
        if not module.check_mode:
            result['json'] = create_pull_request(module, bitbucket)
        result['changed'] = True
    # Delete pull request
    elif existing_pulls and (state == 'absent'):
        for d in existing_pulls:
            if d.get('toRef', 'non_existing_pull_to_branch')['displayId'] == module.params['to_branch'] and \
                   d.get('fromRef', 'non_existing_pull_to_branch')['displayId'] == module.params['from_branch']:
                if not module.check_mode:
                    result['json'] = delete_pull_request(module, bitbucket, d.get('id'), d.get('version'))
                result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()