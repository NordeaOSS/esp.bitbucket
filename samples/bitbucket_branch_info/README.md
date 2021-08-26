# Overview

This sample shows how to retrieve Bitbucket repository branches using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve all branches] *******************************************************
ok: [localhost]

TASK [debug] ***********************************************************************
ok: [localhost] => {
    "_result": {
        "branches": [
            {
                "displayId": "master",
                "id": "refs/heads/master",
                "isDefault": true,
                "latestChangeset": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "latestCommit": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "type": "BRANCH"
            },
            {
                "displayId": "feature/abc",
                "id": "refs/heads/feature/abc",
                "isDefault": false,
                "latestChangeset": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "latestCommit": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "type": "BRANCH"
            },
            {
                "displayId": "develop",
                "id": "refs/heads/develop",
                "isDefault": false,
                "latestChangeset": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "latestCommit": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "type": "BRANCH"
            }
        ],
        "changed": false,
        "failed": false,
        "filter": [
            "*"
        ],
        "messages": [],
        "project_key": "FOO",
        "repository": "bar"
    }
}

TASK [Retrieve the branches matching the supplied branch filters] ******************
ok: [localhost]

TASK [debug] ***********************************************************************
ok: [localhost] => {
    "_result": {
        "branches": [
            {
                "displayId": "develop",
                "id": "refs/heads/develop",
                "isDefault": false,
                "latestChangeset": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "latestCommit": "93b84625d75123b7f7942fd72225400fa66d62ec",
                "type": "BRANCH"
            }
        ],
        "changed": false,
        "failed": false,
        "filter": [
            "develop",
            "feature"
        ],
        "messages": [],
        "project_key": "FOO",
        "repository": "bar"
    }
}
```