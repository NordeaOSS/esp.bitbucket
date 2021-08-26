#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Paweł Smolarz <pawel.smolarz@nordea.com>
# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: bitbucket_push
short_description: Commit and push changes to the remote repository
description: 
- Pushes changes to remote Bitbucket repository.
- Optionally, before pushing changes, it creates a new commit containing the current contents of the index and the working tree.
- Returns the commit hash.
- Authentication can be done with I(token) or with I(username) and I(password).
author:
  - Pawel Smolarz (pawel.smolarz@nordea.com) 
  - Krzysztof Lewandowski (@klewan)
version_added: 1.3.1
options:
  commit:
    description:
    - Commit changes before pushing to the remove repository.
    type: bool
    default: yes
  repodir:
    description:
    - Repository directory.
    - This must be a valid git repository.
    type: str  
    aliases: [ path ]         
    required: true    
  msg:
    description:
    - Log message describing the changes.
    type: str
    required: true
  committer:
    description:
    - A person who commits the code.      
    type: dict
    required: true      
    suboptions:
      name:
        description:
        - The committer username.
        type: str
        required: true    
      email:
        description:
        - The committer email address.
        type: str
        required: true
  tag:
    description:
    - Opitionally add a tag to the commit.
    type: str
    required: false  
  delete:
    description:
    - Delete local repository after push to remote.
    type: bool
    default: no
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
- name: Commit and push changes to the remote repository
  esp.bitbucket.bitbucket_push:
    url: 'https://bitbucket.example.com'
    username: jsmith
    password: secrect
    repository: bar
    project_key: FOO
    path: /tmp/bar  
    commit: yes  
    msg: New commit message
    committer:
      name: jsmith
      email: jsmith@example.com
    tag: '0.3.1'
    delete: no
    validate_certs: no
  register: _result
'''


RETURN = r'''
changed:
    description: Whether or not changes were pushed to a remote repository.
    returned: success
    type: bool
    sample: true
json:
    description: Dictionary with change details.
    returned: success
    type: dict
    contains:
        author:
            description: Commit request author.
            returned: success
            type: dict
            sample:
                email: john.smith@example.com
                name: jsmith
        committer:
            description: Committer.
            returned: success
            type: dict
            sample:
                email: john.smith@example.com
                name: jsmith
        msg:
            description: Commit message.
            returned: success
            type: str
            sample: Commit message    
        before_commit_hexsha:
            description: A commit hash of the working tree before changes were committed.
            returned: success
            type: str
            sample: "c1bd91851a8f5b2b147d252ba674329773e7f675"                      
        after_commit_hexsha:
            description: New commit hash. Exposed only when changes were actually committed, i.e. when C(changed=true).
            returned: success
            type: str
            sample: "06bdcc6594831af4fe869b87643efc609d7cd994" 
        tag:
            description: Commit tag.
            returned: success
            type: str
            sample: '0.3.1'
        deleted:
            description: Whether the local repository was deleted after push to remote.
            returned: success
            type: bool
            sample: false
'''

import os
import shutil

from git import Actor
from git.repo.base import Repo
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper
from ansible.module_utils.common.text.converters import to_native


def main():
    argument_spec = BitbucketHelper.bitbucket_argument_spec()
    argument_spec.update(
        repository=dict(type='str', required=True, no_log=False),
        project_key=dict(type='str', required=True, no_log=False, aliases=['project']),
        commit=dict(type='bool', no_log=False, default=True),
        delete=dict(type='bool', no_log=False, default=False),
        msg=dict(type='str', required=False, no_log=False, aliases=['message']),
        repodir=dict(type='str', required=True, no_log=False, aliases=['path']),
        committer=dict(
            type='dict', 
            required=False, no_log=False,
            options=dict(
                email=dict(type='str', required=True, no_log=False),
                name=dict(type='str', required=True, no_log=False),
            ),            
        ),
        tag=dict(type='str', required=False, no_log=False),        
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,    
        required_together=[('username', 'password')],
        required_one_of=[('username', 'token')],
        mutually_exclusive=[('username', 'token')],
        required_if=[('commit', True, ('committer', 'msg'))],
    )

    bitbucket = BitbucketHelper(module)

    module.params['return_content'] = True

    project_key = module.params['project_key']
    repository = module.params['repository'] 
    msg = module.params['msg']
    committer = module.params['committer']
    commit = module.params['commit']
    repodir = module.params['repodir']
    tag = module.params['tag']
    actor_author = Actor( committer['name'], committer['email'] )
    actor_committer = Actor( committer['name'], committer['email'] )    

    # Seed the result dict in the object
    result = dict(
        changed=False,
        repository=repository,
        project_key=project_key,
        repodir=repodir,
        json=dict(
            author=dict(
                name=committer['name'],
                email=committer['email'],
            ),
            committer=dict(
                name=committer['name'],
                email=committer['email'],
            ),
            msg=msg,
            tag=tag,
            deleted=False,
        )
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

    # Check if repodir exists
    #
    if os.path.exists(repodir):
        try:
            # Internally validates whether the path points to an actual repo.
            repo = Repo(repodir)            
        except Exception as e:
            module.fail_json(msg='%s is not a valid git repository. Details: %s' % (repodir, to_native(e)))
    else:
        module.fail_json(msg='Path %s does not exist.' % (repodir))

    diffs_last_commit_working_tree = False
    if repo.heads:
        result['json']['before_commit_hexsha'] = repo.head.commit.hexsha
        if len(repo.head.commit.diff(None)) > 0:
            diffs_last_commit_working_tree = True

    # When requested, commit all pending changes
    #
    if commit:
        # Set 'changed'=True when there are untracked files or diffs between tree (last commit) and working tree
        #
        if repo.untracked_files or diffs_last_commit_working_tree:
            # It this case, we need to commit changes
            result['changed'] = True

            if not module.check_mode:

                # Add untracked files to index
                for file_add in repo.untracked_files:   
                    repo.index.add([ file_add ])

                # Add only diffs between index and working tree
                for diff in repo.index.diff(None):
                    repo.index.add( list(set( [i for i in [ diff.a_path, diff.b_path ] if i] )) )

                if tag is not None: 
                    repo.create_tag(tag)

                repo.index.commit(msg, author=actor_author, committer=actor_committer)
                result['json']['after_commit_hexsha'] = repo.head.commit.hexsha

    # When repo is without remote, we need to create one
    #
    if len(repo.remotes) == 0:
        result['changed'] = True
        if not module.check_mode:
            repo.create_remote('origin', url="%s/scm/%s/%s.git" % (module.params['url'], project_key, repository) )

    # Push changes to the remote repository
    #
    refspec = repo.active_branch.name + ":" + repo.active_branch.name

    git_askpass_script = bitbucket.create_git_askpass_script()
    if module.params['token']:
        git_password = module.params['token']
    else:
        git_password = module.params['password']

    if not module.check_mode:
        
        with repo.git.custom_environment(GIT_CONFIG_NOSYSTEM="true", GIT_USERNAME=module.params['username'], GIT_PASSWORD=git_password, GIT_ASKPASS=git_askpass_script):
            push_info = repo.remotes.origin.push(refspec=refspec)

        if not push_info[0].summary.count("up to date"):
            result['changed'] = True

    os.unlink( git_askpass_script )

    # Delete the local repository, when requested
    #
    if module.params['delete']:
        result['changed'] = True
        result['json']['deleted'] = True
        if not module.check_mode:
            shutil.rmtree(repodir, ignore_errors=True)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
 