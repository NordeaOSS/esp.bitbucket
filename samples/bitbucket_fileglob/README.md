# Overview

This sample shows how to retrieve a list of files from particular repository of a Bitbucket Server.

It uses `esp.bitbucket.bitbucket_fileglob` lookup.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Display paths of all files in a repository - returns a true list] *******************************************************
ok: [localhost] => {
    "msg": [
        "path/to/dir1/vault.yml",
        "path/to/dir2/file.txt",
        "qux.txt",
        "path/to/dir1/baz.yml"
    ]
}

TASK [Display paths of all files from a repository that end specific way - returns a string list of paths joined by commas] ***
ok: [localhost] => {
    "msg": "path/to/dir1/vault.yml,path/to/dir2/file.txt,qux.txt,path/to/dir1/baz.yml"
}

TASK [Display paths of all files with 'baz' in their names in develop branch - returns a true list] ***************************
ok: [localhost] => {
    "msg": [
        "path/to/dir1/baz.yml"
    ]
}




TASK [Add a line to a report file for each file found in the specified directories on Bitbucket repository] ***********
changed: [localhost] => (item=[Processing path/to/dir1/baz.yml file from Bitbucket Server ..])
changed: [localhost] => (item=[Processing path/to/dir1/vault.yml file from Bitbucket Server ..])
changed: [localhost] => (item=[Processing path/to/dir2/file.txt file from Bitbucket Server ..])
```