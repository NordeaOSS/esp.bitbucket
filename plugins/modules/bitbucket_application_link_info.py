#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_application_link_info
short_description: Retrieve application links
description:
- Search for application links on Bitbucket Server.
- One may refer to an application link either by its ID or its name.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
version_added: 1.2.0
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
  applink:
    description:
    - Retrieve application links matching the supplied I(applink) filter.
    - This can be '*' which means all application links.
    - One may refer to an application link either by its ID or its name.    
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
- name: Retrieve details on the given application links (supplied by names or IDs)
  esp.bitbucket.bitbucket_application_link_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    applink:
      - FOO
      - 227dd1d7-f6d6-34a5-b046-5663fb518691
    validate_certs: no

- name: Retrieve details on all application links
  esp.bitbucket.bitbucket_application_link_info:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    applink:
      - '*'
    validate_certs: no
'''

RETURN = r'''
applicaton_links:
    description: List of application links data.
    returned: always
    type: list
    elements: dict
    sample:
        - data: {}
          displayUrl: https://terraform.example.com/my-org
          id: 227dd1d7-f6d6-34a5-b046-5663fb518691
          name: Terraform (my-org)
          primary: false
          properties: {}
          rpcUrl: https://terraform.example.com/app/my-org
          system: false
          type: generic
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        applink=dict(type='list', elements='str', no_log=False, default=[ '*' ]),
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

    # Parse `applink` parameter and create list of application links.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '*' which means all application links.
    applinks = []
    applinks = [p.strip() for p in module.params['applink']]
    applinks = bitbucket.listify_comma_sep_strings_in_list(applinks)
    if not applinks:
        applinks = [ '*' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        applicaton_links=[],
    )

    # Retrieve detalis on all Application Links
    all_applinks = bitbucket.get_application_links_info()
    
    if '*' in applinks:
        result['applicaton_links'].extend( all_applinks['json'] )
    else:    
        for applink in applinks:
            found = [al for al in all_applinks['json'] if al['id'] == applink or al['name'] == applink]
            if len(found) == 1:
                result['applicaton_links'].append( found[0] )

    module.exit_json(**result)


if __name__ == '__main__':
    main()