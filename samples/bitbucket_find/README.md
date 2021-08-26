# Overview

This sample shows how to retrieve a list of files from particular repository of a Bitbucket Server.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve paths of all files in a repository in develop branch that end specific way] ********
ok: [localhost]

TASK [debug] **************************************************************************************
ok: [localhost] => {
    "_result": {
        "at": "develop",
        "changed": false,
        "failed": false,
        "files": [
            "path/to/baz.yml",
            "path/to/vault.yml"
        ],
        "grep": null,
        "messages": [],
        "patterns": [
            ".+\\.yml$",
            ".+\\.json$"
        ],
        "project_key": "FOO",
        "repository": "bar"
    }
}

TASK [Retrieve paths of all files with 'baz' in their names in develop branch and with the supplied grep pattern in the files content] ********
ok: [localhost]

TASK [debug] **************************************************************************************
ok: [localhost] => {
    "_result": {
        "at": "develop",
        "changed": false,
        "failed": false,
        "files": [
            "path/to/baz.yml"
        ],
        "grep": "hello.+?world",
        "messages": [],
        "patterns": [
            "baz"
        ],
        "project_key": "FOO",
        "repository": "bar"
    }
}
```