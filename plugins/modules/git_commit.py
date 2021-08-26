#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Paweł Smolarz <pawel.smolarz@nordea.com>
# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: git_commit
short_description: Commit changes to the local repository
description: 
- Creates a new commit containing the current contents of the index and the working tree.
- Returns the commit hash.
author:
  - Pawel Smolarz (pawel.smolarz@nordea.com) 
  - Krzysztof Lewandowski (@klewan)
version_added: 1.3.1
options:
  repository:
    description:
    - Repository name.
    type: str
    required: true
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
notes:
- requirements [ os, pathlib, gitpython ]
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Commit changes to the local repository
  esp.bitbucket.git_commit:  
    repository: repo
    path: /tmp/repo    
    msg: New commit message
    committer:
      name: jsmith
      email: jsmith@example.com
    tag: '0.3.1'
  register: _result
'''

RETURN = r'''
changed:
    description: Whether or not changes were committed.
    returned: success
    type: bool
    sample: true
json:
    description: Dictionary with commit details.
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
'''

import os
from git import Actor
from git.repo.base import Repo
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text


def main():
    module = AnsibleModule(
        argument_spec=dict(
            repository=dict(type='str', required=True, no_log=False),
            msg=dict(type='str', required=True, no_log=False, aliases=['message']),
            repodir=dict(type='str', required=True, no_log=False, aliases=['path']),
            committer=dict(
                type='dict', 
                required=True, no_log=False,
                options=dict(
                    email=dict(type='str', required=True, no_log=False),
                    name=dict(type='str', required=True, no_log=False),
                ),            
            ),
            tag=dict(type='str', required=False, no_log=False),
        ),
        supports_check_mode=True, 
    )

    repository = module.params['repository']
    msg = module.params['msg']
    committer = module.params['committer']
    repodir = module.params['repodir']
    tag = module.params['tag']
    actor_author = Actor( committer['name'], committer['email'] )
    actor_committer = Actor( committer['name'], committer['email'] )    

    # Seed the result dict in the object
    result = dict(
        changed=False,
        repository=repository,
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
        )
    )

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

    module.exit_json(**result)


if __name__ == '__main__':
    main()
 