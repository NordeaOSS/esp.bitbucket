# Overview

This sample shows how set default branch on remote Bitbucket repository using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Set branch as default] ************************************************************
changed: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "branch": "develop",
        "changed": true,
        "failed": false,
        "isDefault": true,
        "json": {
            "fetch_url_retries": 1
        },
        "project_key": "FOO",
        "repository": "bar"
    }
}
```