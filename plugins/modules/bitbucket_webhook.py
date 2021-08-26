#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Pawel Smolarz <pawel.smolarz@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bitbucket_webhook
short_description: Manage repository webhooks on Bitbucket Server
description:
- Manages repository webhooks on Bitbucket Server.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
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
  webhook_name:
    description:
    - Webhook name to create
    type: str
    default: wh_<repo>
    required: true
    aliases: [ wh_name ]
  webhook_url:
    description:
    - Webhook url
    type: str
    default: https://jenkins.example.com/bitbucket-hook/
    required: true
    aliases: [ wh_url ]
  event:
    description:
    - Webhook events list seperated by comma
    type: str
    default: repo:refs_changed
    required: true
  state:
    description:
    - Whether the webhook should exist or not.
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
- name: Create webhook
  esp.bitbucket.bitbucket_webhook:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    validate_certs: no
    state: present
    webhook_name: wh_repo1
    webhook_url: "https://jenkins.example.com/bitbucket-hook/"
    event: "repo:refs_changed"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def create_webhook(module, bitbucket):
    info, content = bitbucket.request(
        api_url=bitbucket.BITBUCKET_API_ENDPOINTS['webhooks'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
        ),
        method='POST',
        data={
            'name': module.params['webhook_name'],
            'url':  module.params['webhook_url'],
            'events': module.params['event'].split(','),
            'active': 'true'
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

    return None

def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        webhook_name=dict(type='str', default='develop', aliases=['wh_name']),
        webhook_url=dict(type='str', default='https://jenkins.example.com/bitbucket-hook/', aliases=['wh_url']),
        event=dict(type='str', default='repo:refs_changed', aliases=['wh_event']),
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
    webhook_name = module.params['webhook_name']
    return_content = module.params['return_content']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],
        repository=module.params['repository'],
        state=module.params['state'],
        webhook_name=module.params['webhook_name'],
        parsed_event=module.params['event'].split(','),
        # parsed_event=bitbucket.listify_comma_sep_strings_in_list(module.params['event']),
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

    # Retrieve existing webhooks information (if any)
    existing_webhooks = bitbucket.get_webhooks_info(fail_when_not_exists=False, filter=None)

    # Create new webhook in case it does not exist
    if (state == 'present') and \
            (not any(d.get('name', 'non_existing_webhook') == webhook_name for d in existing_webhooks)):
        if not module.check_mode:
            result['json'] = create_webhook(module, bitbucket)
        result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()