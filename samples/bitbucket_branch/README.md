# Overview

This sample create remote branch on Bitbucket repository using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Create branch develop from master] ************************************************
changed: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "branch": "develop",
        "changed": true,
        "failed": false,
        "from_branch": "master",
        "is_default": true,
        "json": {
            "displayId": "develop",
            "fetch_url_retries": 1,
            "id": "refs/heads/develop",
            "isDefault": false,
            "latestChangeset": "3abe5c0295284389a6e620bf01203efbbf166d80",
            "latestCommit": "3abe5c0295284389a6e620bf01203efbbf166d80",
            "type": "BRANCH"
        },
        "project_key": "FOO",
        "repository": "bar",
        "state": "present"
    }
}
```