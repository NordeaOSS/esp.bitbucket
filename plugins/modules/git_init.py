#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Paweł Smolarz <pawel.smolarz@nordea.com>
# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: git_init
short_description: Initialize local empty repository
description: 
- Initializes local empty repository.
author:
  - Pawel Smolarz (pawel.smolarz@nordea.com) 
  - Krzysztof Lewandowski (@klewan)
version_added: 1.3.0
options:
  repodir:
    description:
    - Repository directory.
    type: str  
    aliases: [ path ] 
    required: true  
  force:
    description:
    - Force initalization, i.e. delete the repo directory if it already exists, then initialize.
    type: bool
    default: no  
    required: false      
notes:
- requirements [ os, pathlib, gitpython ]
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Initialize git repository
  esp.bitbucket.git_init:  
    path: /tmp/bar 
    force: no   
  register: _result

- name: Initialize git repository, but first delete the directory if it exists
  esp.bitbucket.git_init:  
    path: /tmp/bar 
    force: yes   
  register: _result
'''

RETURN = r'''
changed:
    description: Whether or not repository has been initialized.
    returned: success
    type: bool
    sample: true
'''

import os
import shutil

from git.repo.base import Repo
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def main():
    module = AnsibleModule(
        argument_spec=dict(
            repodir=dict(type='str', required=True, no_log=False, aliases=['path']),
            force=dict(type='bool', no_log=False, default=False),
        ),
        supports_check_mode=True, 
    )

    repodir = module.params['repodir']  
    force = module.params['force']  

    # Seed the result dict in the object
    result = dict(
        changed=False,
        repodir=repodir,
        force=force,
    )

    # Delete repodir if it exists and force=True
    #
    if os.path.exists(repodir) and force:

        if os.path.isdir(repodir):

            result['changed'] = True
            if not module.check_mode:
                try:
                    shutil.rmtree(repodir, ignore_errors=True)          
                except Exception as e:
                    module.fail_json(msg='Error while deleting %s directory. Details: %s' % (repodir, to_native(e)))
        else:
            module.fail_json(msg='Path %s exists and is not a directory.' % (repodir))

    # Check if repodir exists
    #
    if not os.path.exists(repodir):
        
        if not module.check_mode:

            try:  
                Repo.init(repodir)   
            except Exception as e:
                module.fail_json(msg='Failed to initialize git repository in %s path. Details: %s' % (repodir, to_native(e)))

        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
 