# Overview

This sample shows how to create and delete Bitbucket projects on Bitbucket Server using ESP Bitbucket Ansible modules.
The sample can be modified to include a project avatar.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Create Bitbucket project] *******************************
changed: [localhost]

TASK [debug] **************************************************
ok: [localhost] => {
    "_result": {

        "changed": true,
        "description": "This is a new Bitbucket project",
        "failed": false,
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
    }
}

TASK [Delete Bitbucket project] *******************************
changed: [localhost]

TASK [debug] **************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false
    }
} 
```