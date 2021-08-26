#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_copy
short_description: Copy files to Bitbucket Server
description:
- The C(bitbucket_copy) module copies (pushes) a file from the local machine to a Bitbucket Server repository.
- Creates the file if it does not exist.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Krzysztof Lewandowski (@klewan)
version_added: 1.1.0
options:
  src:
    description:
    - Local path to a file to copy to the Bitbucket Server repository.
    - This can be absolute or relative.
    - Required when U(content) is not provided.
    type: path
    required: false    
  content:
    description:
    - When used instead of C(src), sets the contents of a file directly to the specified value.
    - Required when U(src) is not provided.    
    type: str
    required: false      
  dest:
    description:
    - Path in Bitbucket repositorywhere the file should be copied to.
    type: path
    required: yes
  message:
    description:
    - Commit message.
    - If not specified the default message should be used.
    type: str
    required: false
  branch:
    description:
    - The branch to write a file at.
    - If not specified the default branch will be used instead.
    type: str
    required: false
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
- name: Copy file to Bitbucket
  esp.bitbucket.bitbucket_copy:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    src: /tmp/baz.yml
    dest: path/to/baz.yml
    message: File updated using bitbucket_copy module
    branch: master
    validate_certs: no
    force_basic_auth: yes

- name: Copy file to Bitbucket using inline content
  esp.bitbucket.bitbucket_copy:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    content: '# Hello world'
    dest: path/to/baz.yml
    message: File updated using bitbucket_copy module
    branch: master
    validate_certs: no
    force_basic_auth: yes
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
branch:
    description: Branch name.
    returned: always  
    type: str
    sample: master
dest:
    description: Path in Bitbucket repositorywhere the file was copied to.
    returned: always  
    type: str
    sample: path/to/baz.yml
src:
    description: Local path to a file which was copied to the Bitbucket Server repository.
    returned: success  
    type: str
    sample: /tmp/baz.yml
json:
    description: Dictionary with updated file details.
    returned: success
    type: dict
    contains:
        author:
            description: Commit request author.
            returned: success
            type: dict
            sample:
                active: true
                displayName: John Smith
                emailAddress: john.smith@example.com
                id: 5719
                links:
                    self:
                        - href: https://bitbucket.example.com/users/jsmith
                name: jsmith
                slug: jsmith
                type: NORMAL
        committer:
            description: Committer.
            returned: success
            type: dict
            sample:
                active: true
                displayName: John Smith
                emailAddress: john.smith@example.com
                id: 5719
                links:
                    self:
                        - href: https://bitbucket.example.com/users/jsmith
                name: jsmith
                slug: jsmith
                type: NORMAL
        authorTimestamp:
            description: Timestamp.
            returned: success
            type: int
            sample: 1618819213000            
        committerTimestamp:
            description: Timestamp.
            returned: success
            type: int
            sample: 1618819213000
        message:
            description: Commit message.
            returned: success
            type: str
            sample: "File updated using bitbucket_copy module"     
        id:
            description: Commit id.
            returned: success
            type: str
            sample: "2525b8cc320c6c5c71a84d1c21f0554b012214df"                      
        displayId:
            description: Commit id.
            returned: success
            type: str
            sample: "2525b8cc320"              
'''


import os
import os.path
import hashlib

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper
from ansible.module_utils._text import to_bytes, to_native
from ansible.module_utils.urls import prepare_multipart


def copy_file(module, bitbucket, src_content=None, sourceCommitId=None):
    """
    Copy file to Bitbucket Server

    """
    body = {
        'content': src_content,
    }
    if module.params['branch'] is not None:
        body['branch'] = module.params['branch']
    if module.params['message'] is not None:
        body['message'] = module.params['message']
    if sourceCommitId is not None:
        body['sourceCommitId'] = sourceCommitId

    url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-browse'] 
          + '/{path}').format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['dest'],
    )

    try:
        content_type, body = prepare_multipart(body)
    except (TypeError, ValueError) as e:
        module.fail_json(msg='failed to parse body as form-multipart: %s' % to_native(e))

    info, content = bitbucket.request(
        api_url=url,
        method='PUT',
        data=body,
        headers={
            'Content-type': content_type,
        },
    ) 

    if info['status'] == 200:     
        return content

    if info['status'] == 400:
        module.fail_json(msg='The branch or content parameters were not supplied.')    

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user does not have write permission for the given repository.') 

    if info['status'] == 404:
        module.fail_json(msg='The repository does not exist.') 

    if info['status'] == 409:
        module.fail_json(msg='The file already exists when trying to create a file, or the given content does not modify the file, or the file has changed since the given sourceCommitId.') 

    if info['status'] != 200:
        module.fail_json(
            msg='Failed update file in `{repositorySlug}` repository: {info}'.format(
                repositorySlug=module.params['repository'],
                info=info,
            ))

    return None


def get_latest_commit(module, bitbucket):
    """
    Return the latest commit information for the supplied file from Bitbucket Server

    """
    since_until = ""
    if module.params['branch'] is not None:
        branch_info = bitbucket.get_branches_info(fail_when_not_exists=False, filter=module.params['branch'])

        if branch_info is not None:
            try:
                since_until = "&until=" + branch_info[0]['latestCommit']
            except Exception as e:
                raise AnsibleError('Unable to retrieve "%s" branch information: %s' % (module.params['branch'], to_native(e)))


    url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-commits'] 
          + '?limit=1&followRenames=true&ignoreMissing=true&merges=include&path={path}{since_until}').format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['dest'],
            since_until=since_until,
    )

    info, content = bitbucket.request(
        api_url=url,
        method='GET',
    )
    
    if info['status'] == 200:
        try:
            latest_commit_id = content['values'][0]['id']
        except Exception as e:
            raise AnsibleError('Unable to retrieve latest commit id of "%s" branch: %s' % (module.params['branch'], to_native(e)))      
        return latest_commit_id

    if info['status'] == 400:
        module.fail_json(msg='One of the supplied commit IDs or refs was invalid.')    

    if info['status'] == 401:
        module.fail_json(msg='The currently authenticated user has insufficient permissions to view the repository.') 

    if info['status'] == 404:
        module.fail_json(msg='The repository does not exist.') 

    return None


def get_dest_md5(module, bitbucket):
    """
    Return file content md5 from Bitbucket Server

    """
    at = ""
    if module.params['branch'] is not None:
        at = "?at=%s" % module.params['branch']

    info, content = bitbucket.request(
        api_url=BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-raw-path'].format(
            url=module.params['url'],
            projectKey=module.params['project_key'],
            repositorySlug=module.params['repository'],
            path=module.params['dest'],
            at=at,
        ),
        method='GET',
    )

    if info['status'] == 200:
        if 'content' in content:
            file_content = content['content']
        else:
            file_content = content
        return hashlib.md5(str(file_content).encode('utf-8')).hexdigest()        
    else:
        return None


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        src=dict(type='path', required=False, no_log=False),
        content=dict(type='str', required=False, no_log=True),
        dest=dict(type='path', required=True, no_log=False),
        branch=dict(type='str', required=False, no_log=False),
        message=dict(type='str', required=False, no_log=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token'), ('src', 'content')],
        mutually_exclusive=[('username', 'token')]
    )

    bitbucket = BitbucketHelper(module)

    # Check if project and repository exist.
    if not bitbucket.get_project_info(fail_when_not_exists=False, project_key=module.params['project_key']):
        msg = 'Project `{projectKey}` does not exist.'.format(
            projectKey=module.params['project_key']
        )
        module.fail_json(msg=msg)
    if not bitbucket.get_repository_info(fail_when_not_exists=False, project_key=module.params['project_key'], repository=module.params['repository']):
        msg = 'Repository `{repositorySlug}` does not exist.'.format(
            repositorySlug=module.params['repository']
        )
        module.fail_json(msg=msg)

    # Seed the result dict in the object
    result = dict(
        changed=False,
        project_key=module.params['project_key'],        
        repository=module.params['repository'],
        dest=module.params['dest'],
        json={},
    )
    if module.params['src'] is not None:
        result['src'] = module.params['src']
    if module.params['branch'] is not None:
        result['branch'] = module.params['branch']

    src = module.params['src']
    if src is not None:
        b_src = to_bytes(src, errors='surrogate_or_strict')

        if not os.path.exists(b_src):
            module.fail_json(msg="Source %s not found" % (src))
        if not os.access(b_src, os.R_OK):
            module.fail_json(msg="Source %s not readable" % (src))
        if not os.path.isfile(src):
            module.fail_json(msg="Source %s not a file" % (src))

        with open(b_src, 'rb') as f:
            src_content = f.read()

        src_md5 = hashlib.md5(str(src_content).encode('utf-8')).hexdigest()
    else:
        src_content = module.params['content']
        src_md5 = hashlib.md5(str(src_content).encode('utf-8')).hexdigest()   

    # Return md5 of an existing file content in Bitbucket repository, if the file exists
    dest_md5 = get_dest_md5(module, bitbucket)

    if dest_md5 is not None:
        # If the file in Bitbucket repository exists, upload it only when checksums differ
        if dest_md5 != src_md5:
            if not module.check_mode:
                sourceCommitId = get_latest_commit(module, bitbucket)
                result['json'] = copy_file(module, bitbucket, src_content=src_content, sourceCommitId=sourceCommitId)
            result['changed'] = True
    else:
        # If the file in Bitbucket repository does not exist, just upload it
        if not module.check_mode:
            result['json'] = copy_file(module, bitbucket, src_content=src_content, sourceCommitId=None)
        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()