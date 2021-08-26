# Overview

This sample shows how to grant or revoke Bitbucket project permissions using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Set PROJECT_WRITE permission level for the specified project to jsmith user] ****************
changed: [localhost]

TASK [debug] **************************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "json": {
            "fetch_url_retries": 1
        },
        "messages": [],
        "permission": "PROJECT_WRITE",
        "project_key": "FOO",
        "user": "jsmith"
    }
}

TASK [Revoke all permissions for the specified project from a group] ******************************
changed: [localhost]

TASK [debug] **************************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "group": "dev-group",
        "json": {
            "fetch_url_retries": 1
        },
        "messages": [],
        "permission": "",
        "project_key": "FOO"
    }
}
```