# Overview

This sample shows how to create and delete Bitbucket repositories on Bitbucket Server using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Create Bitbucket repository] ***************************************************
changed: [localhost]

TASK [debug] *************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "forkable": true,
        "hierarchyId": "aa48b8baedb8216fa47e",
        "id": 168,
        "links": {
            "clone": [
                {
                    "href": "https://bitbucket.example.com/scm/foo/bar.git",
                    "name": "http"
                },
                {
                    "href": "ssh://git@bitbucket.example.com:7999/foo/bar.git",
                    "name": "ssh"
                }
            ],
            "self": [
                {
                    "href": "https://bitbucket.example.com/projects/FOO/repos/bar/browse"
                }
            ]
        },
        "name": "bar",
        "project": {
            "description": "This is a new Bitbucket project",
            "id": 292,
            "key": "FOO",
            "links": {
                "self": [
                    {
                        "href": "https://bitbucket.example.com/projects/FOO"
                    }
                ]
            },
            "name": "A new Bitbucket project",
            "public": false,
            "type": "NORMAL"
        },
        "public": false,
        "scmId": "git",
        "slug": "bar",
        "state": "AVAILABLE",
        "statusMessage": "Available"
    }
}

TASK [Delete Bitbucket repository] ***************************************************
changed: [localhost]

TASK [debug] *************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "context": null,
        "exceptionName": null,
        "failed": false,
        "message": "Repository scheduled for deletion."
    }
} 
```