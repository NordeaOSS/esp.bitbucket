# Overview

This sample shows how get information about pull requests on Bitbucket repository using ESP Bitbucket Ansible modules.

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

TASK [Get pull requests on repository] ***************************************************************************************************************************************************************************
ok: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_pull_info_output": {
        "changed": false,
        "failed": false,
        "json": [
            {
                "author": "m00001",
                "fromRef": "pull_test",
                "pull_id": 17,
                "title": "Test pull",
                "toRef": "master",
                "version": 0
            },
            {
                "author": "m00001",
                "fromRef": "develop",
                "pull_id": 16,
                "title": "Test pull2",
                "toRef": "master",
                "version": 0
            }
        ],
        "messages": [],
        "project_key": "APITEST",
        "repository": "repo01"
    }
}


```