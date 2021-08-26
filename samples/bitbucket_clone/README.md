# Overview

This sample shows how to clone remote Bitbucket repository and push changes using ESP Bitbucket Ansible modules.

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

TASK [Clone repository] ******************************************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "msg": [
            "Repository cloned: bar"
        ]
    }
}

TASK [ansible.builtin.file] **************************************************************************************************************************************************************************************
changed: [localhost] => (item=test_fe1.txt)
changed: [localhost] => (item=test_fe2.txt)
changed: [localhost] => (item=test_fe3.txt)

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
            "Repository bar pushed to Bitbucket."
        ]
    }
}

```