# Overview

This sample shows how create webhook on Bitbucket repository using ESP Bitbucket Ansible modules.

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

TASK [Create webhook on repository] ******************************************************************************************************************************************************************************
ok: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_create_output": {
        "changed": false,
        "failed": false,
        "json": {},
        "messages": [],
        "parsed_event": [
            "repo:refs_changed",
            "repo:modified"
        ],
        "project_key": "PROJECT",
        "repository": "test",
        "state": "present",
        "webhook_name": "wh_test"
    }
}

```