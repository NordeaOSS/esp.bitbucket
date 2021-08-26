# Overview

This sample shows how to create empty repository and initialize locally repository for Bitbucket Server using ESP Bitbucket Ansible modules.

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
```