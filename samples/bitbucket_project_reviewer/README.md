# Overview

This sample shows how setup default reviewers on Bitbucket project using ESP Bitbucket Ansible modules.
In this is possible to protect projects and eg. master branch for all repositories defined inside project.

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

TASK [Configure default reviewer on project level] ***************************************************************************************************************************************************************
ok: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_project_reviewer": {
        "changed": false,
        "failed": false,
        "json": {},
        "messages": [],
        "project_key": "APITEST",
        "state": "present"
    }
}

```