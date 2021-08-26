# Overview

This sample shows how to grant or revoke Bitbucket repository permissions using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Set REPO_WRITE permission level for the specified repository to jsmith user] ******
changed: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "json": {},
        "messages": [],
        "permission": "REPO_WRITE",
        "project_key": "FOO",
        "repository": "bar",
        "user": "jsmith"
    }
}     

TASK [Revoke all permissions for the specified repository from a group] *****************
changed: [localhost]

TASK [debug] ****************************************************************************
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
        "project_key": "FOO",
        "repository": "bar"
    }
}
```