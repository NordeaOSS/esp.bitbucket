#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_find
short_description: Retrieve a list of files from particular repository of a Bitbucket Server based on specific criteria
description:
- Retrieve a list of matching file names from particular repository of a Bitbucket Server. 
- Files are selected based on C(patterns) option. Additionaly, files can be further filtered out by C(grep) option to select only those matching the supplied grep pattern.
- Combined outcome of C(patterns) and C(grep) options form the final list of files returned by this module.
- The search is done using Python regex patterns.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
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
    aliases: [ name ]
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
    aliases: [ project ]  
  at:
    description:
    - The commit ID or ref (e.g. a branch or tag) to read a file at.
    - If not specified the default branch will be used instead.
    type: str
    required: false
  patterns:
    default: []
    description:
    - List of Python regex patterns to search for in file names on a Bitbucket Server repository.
    - The patterns restrict the list of files to be returned to those whose basenames match at
      least one of the patterns specified. Multiple patterns can be specified using a list.
    - This parameter expects a list, which can be either comma separated or YAML. If any of the
      patterns contain a comma, make sure to put them in a list to avoid splitting the patterns
      in undesirable ways.
    - Defaults to '.+'.
    type: list
    aliases: [ pattern ]
    elements: str
  grep:
    description:
    - Python regex pattern to search for in each file selected from repository to form the final list of files.
    - Files are selected based on C(patterns) option.
    - Combined outcome of C(patterns) and C(grep) options form the final list of files returned by this module.
    - If not specified, search will not be executed.
    type: str
    aliases: [ search ]    
    required: false  
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
seealso:
- lookup: esp.bitbucket.bitbucket_fileglob
'''

EXAMPLES = r'''
- name: Retrieve paths of all files in a repository at develop branch
  esp.bitbucket.bitbucket_find:
    url: 'https://bitbucket.example.com'
    username: '{{ bitbucket_username }}'
    password: '{{ bitbucket_password }}'
    repository: bar
    project_key: FOO
    at: develop
    validate_certs: no

- name: Retrieve paths of all files in a repository that end specific way
  esp.bitbucket.bitbucket_find:
    url: 'https://bitbucket.example.com'
    username: '{{ bitbucket_username }}'
    password: '{{ bitbucket_password }}'
    repository: bar
    project_key: FOO
    patterns:
      - '.+\.yml$'
      - '.+\.json$'
    validate_certs: no

- name: Retrieve paths of all files with 'baz' in their names in develop branch and with the supplied grep pattern in the files content
  esp.bitbucket.bitbucket_find:
    url: 'https://bitbucket.example.com'
    token: 'MjA2M...hqP58'
    repository: bar
    project_key: FOO
    patterns: baz
    at: develop
    grep: 'hello.+?world'    
    validate_certs: no
'''

RETURN = r'''
repository:
    description: Bitbucket repository name.
    returned: always
    type: str
    sample: bar
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
      - Repository `bar2` does not exist. 
at:
    description: The commit ID or ref (e.g. a branch or tag) to read a file at.
    returned: always  
    type: str
    sample: master
patterns:
    description: List of Python regex patterns to search for in file names on a Bitbucket Server repository.
    returned: always
    type: list
    sample:
      - ".+\\.yml$"
      - ".+\\.json$"
grep:
    description: Python regex pattern to search for in each file selected from repository to form the final list of files.
    returned: always  
    type: str
    sample: hello      
files:
    description: List of matching file names from particular repository.
    returned: success
    type: list
    sample:
      - path/to/baz.yml
      - path/to/vault.yml
'''

import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper
from ansible.module_utils.six import string_types


def slurp_file(module, bitbucket, project_key=None, repository=None, path=None):
    """
    Read file content on Bitbucket Server

    """
    at = ""
    if module.params['at'] is not None:
        at = "?at=%s" % module.params['at']

    info, content = bitbucket.request(
        api_url=BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-raw-path'].format(
            url=module.params['url'],
            projectKey=project_key,
            repositorySlug=repository,
            path=path,
            at=at,
        ),
        method='GET',
    )

    if info['status'] == 200:
        return content['content']

    if info['status'] != 200:
        module.fail_json(msg='Failed to retrieve content of a file which matches the supplied projectKey `{projectKey}`, repositorySlug `{repositorySlug}` and file path `{path}`: {info}'.format(
            projectKey=project_key,
            repositorySlug=repository,
            path=path,
            info=info,
        ))

    return None


def get_list_of_files(module, bitbucket, project_key=None, repository=None):
    """
    Retrieve a list of all files from particular repository of a Bitbucket Server
    """

    filelist = []
    at = ""
    if module.params['at'] is not None:
        at = "&at=%s" % module.params['at']

    isLastPage = False
    nextPageStart = 0

    while not isLastPage:

        info, content = bitbucket.request(
            api_url=(bitbucket.BITBUCKET_API_ENDPOINTS['repos-files'] + '?limit=1000&start={nextPageStart}{path}{at}').format(
                url=module.params['url'],
                projectKey=project_key,                
                repositorySlug=repository,
                nextPageStart=nextPageStart,
                at=at,
                path='',
            ),
            method='GET',
        )              

        if info['status'] == 200:
            filelist.extend(content['values'])

        if info['status'] == 400:
            raise AnsibleError("The path requested is not a directory at the supplied commit.")

        if info['status'] == 404:
            raise AnsibleError("The specified repository does not exist.")

        if info['status'] != 200:
            raise AnsibleError("Failed to retrieve a list of files Bitbucket Server.  : {info}".format(
                    info=info,
                ))

        if 'isLastPage' in content:
            isLastPage = content['isLastPage']
            if 'nextPageStart' in content:
                nextPageStart = content['nextPageStart']
        else:
            isLastPage = True

    return filelist


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False, aliases=['name']),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),                
        at=dict(type='str', required=False, no_log=False),
        patterns=dict(type='list', default=[], aliases=['pattern'], elements='str'),
        grep=dict(type='str', required=False, no_log=False, aliases=['search']),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    project_key = module.params['project_key'] 
    repository = module.params['repository']
    return_content = module.params['return_content']
    at = module.params['at']
    grep = module.params['grep']

    module.params['return_content'] = True    

    # Parse `patterns` parameter and create list of patterns.
    # It's possible someone passed a comma separated string, so we should handle that.
    # This can be either an empty list or '.+' which means all patterns.
    patterns = []
    patterns = [p.strip() for p in module.params['patterns']]
    patterns = bitbucket.listify_comma_sep_strings_in_list(patterns)
    if not patterns:
        patterns = [ '.+' ]

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=project_key,        
        repository=repository,
        at=at,
        patterns=patterns,
        messages=[],
        files=[],
        grep=grep,
    )

    # Check if project and repository exist. Retrun this message.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=project_key):
        result['messages'].append('Project `{projectKey}` does not exist.'.format(
            projectKey=project_key
        ))
        module.fail_json(msg=result['messages'])
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=project_key, repository=repository):
        result['messages'].append('Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=repository
        ))
        module.fail_json(msg=result['messages'])

    # Retrieve a list of all files from the given repository
    all_files = get_list_of_files(module, bitbucket, project_key=project_key, repository=repository)

    # Compile 'grep' pattern, i.e. PATTERN that is searched in each file selected from repository to form the final list of files
    if grep is not None:
        try:
            grep = re.compile(grep)
        except Exception as e:
            raise AnsibleError('Unable to use "%s" as a search parameter: %s' % (grep, to_native(e)))

    # Itereate over all file patterns
    for input_pattern in patterns:

        if not isinstance(input_pattern, string_types):
            raise AnsibleError('Invalid search pattern, "%s" is not a string, it is a %s' % (input_pattern, type(input_pattern)))

        try:
            pattern = re.compile(input_pattern)
        except Exception as e:
            raise AnsibleError('Unable to use "%s" as a search parameter: %s' % (input_pattern, to_native(e)))

        for file_path in all_files:
            # when file name matches the given pattern
            if pattern.search(file_path):
                # when 'grep' pattern is defined, read the file content
                if grep is not None:
                    file_content = slurp_file(module, bitbucket, project_key=project_key, repository=repository, path=file_path)
                    # when file content matches the given pattern (grep), add the file path to the result list
                    if grep.search(file_content):
                        result['files'].append(file_path)
                else:
                    result['files'].append(file_path)

    # Make the list of files unique
    result['files'] = list(set(result['files']))

    module.exit_json(**result)


if __name__ == '__main__':
    main()