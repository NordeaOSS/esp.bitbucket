#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Paweł Smolarz <pawel.smolarz@nordea.com>
# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_clone
short_description: Clone a repository from Bitbucket Server
description: 
- Clones a repository from Bitbucket Server.
- Returns the latest commit hash of the cloned repository branch.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Pawel Smolarz (pawel.smolarz@nordea.com) 
  - Krzysztof Lewandowski (@klewan)
version_added: 1.3.0
options:
  repodir:
    description:
    - A local destination directory where the repository will be cloned.
    - This must be a valid git repository.
    type: str  
    aliases: [ path ]         
    required: true    
  force:
    description:
    - Delete a local destination directory before cloning, if it already exists.
    type: bool
    default: no  
    required: false     
  branch:
    description:
    - A repository branch to clone.
    type: str
    default: master             
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
    aliases: [ path ] 
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
- requirements [ os, pathlib, gitpython ]
- Supports C(check_mode).
'''


EXAMPLES = r'''
- name: Clone a repository from Bitbucket
  esp.bitbucket.bitbucket_clone:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    branch: master
    path: /tmp/bar  
    force: yes
    validate_certs: no
  register: _result
'''


RETURN = r'''
changed:
    description: Whether or not a repository has been cloned from Bitbucket.
    returned: success
    type: bool
    sample: true
json:
    description: Dictionary with clone details.
    returned: success
    type: dict
    contains:  
        commit_hexsha:
            description: A commit hash of the working tree of the cloned repository branch.
            returned: success
            type: str
            sample: "9074a0e7140e120ae927cb817c0d6fc7ebf6dd37"                      
'''

import os
import shutil

from git.repo.base import Repo
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper
from ansible.module_utils.common.text.converters import to_native


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        branch=dict(type='str', no_log=False, default='master'),
        force=dict(type='bool', no_log=False, default=False),
        repodir=dict(type='str', required=True, no_log=False, aliases=['path']),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')],
    )

    bitbucket = BitbucketHelper(module)

    module.params['return_content'] = True

    project_key = module.params['project_key']
    repository = module.params['repository'] 
    repodir = module.params['repodir']
    branch = module.params['branch']

    # Seed the result dict in the object
    result = dict(
        changed=False,
        repository=repository,
        project_key=project_key,
        repodir=repodir,
        branch=branch,
        json={},
    )

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

    # Delete repodir if it exists and force=True
    #
    if os.path.exists(repodir) and module.params['force']:

        if os.path.isdir(repodir):

            result['changed'] = True
            if not module.check_mode:
                try:
                    shutil.rmtree(repodir, ignore_errors=True)          
                except Exception as e:
                    module.fail_json(msg='Error while deleting %s directory. Details: %s' % (repodir, to_native(e)))
        else:
            module.fail_json(msg='Path %s exists and is not a directory.' % (repodir))

    # Clone repository from Bitbucket
    #
    git_askpass_script = bitbucket.create_git_askpass_script()
    if module.params['token']:
        git_password = module.params['token']
    else:
        git_password = module.params['password']

    remote = "%s/scm/%s/%s.git" % (module.params['url'], project_key, repository)

    if not module.check_mode:
        
        try:
            repo = Repo.clone_from(url=remote, to_path=repodir, branch=branch, env=dict(GIT_CONFIG_NOSYSTEM="true", GIT_USERNAME=module.params['username'], GIT_PASSWORD=git_password, GIT_ASKPASS=git_askpass_script))
        except Exception as e:
            module.fail_json(msg='Error while cloning %s repository. Details: %s' % (remote, to_native(e)))

        result['json']['commit_hexsha'] = repo.head.commit.hexsha
        result['changed'] = True

    os.unlink( git_askpass_script )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
 