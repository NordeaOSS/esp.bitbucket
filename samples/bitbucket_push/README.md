# Overview

This sample shows how push commited changes to remote Bitbucket repository using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
PLAY [A playbook for ansible_bitbucket_project project] **********************************************************************************************************************************************************

TASK [Create empty repository on Bitbucket] **********************************************************************************************************************************************************************
changed: [localhost]

TASK [Initialize locally Bitbucket repository] *******************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_init_output": {
        "changed": true,
        "failed": false,
        "msg": [
            "New repository foo_repo has been successfully initialized"
        ]
    }
} 

TASK [Commit changes to Bitbucket repository] ********************************************************************************************************************************************************************
changed: [localhost]

TASK [Show info from bitbucket_commit module] ********************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": {
        "changed": true,
        "failed": false,
        "msg": [
            "Commit done: TEST COMMIT, ignored files []"
        ]
    }
}

TASK [Push repository to Bitbucket] ******************************************************************************************************************************************************************************
changed: [localhost]

TASK [Show info from bitbucket_push module] **********************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": {
        "changed": true,
        "failed": false,
        "msg": [
            "Repository foo_repo pushed to Bitbucket."
        ]
    }
}
```