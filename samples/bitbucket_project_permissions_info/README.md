# Overview

This sample shows how to retrieve Bitbucket project permissions information using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve Bitbucket project permissions information] *******************************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "filters": [
            "*"
        ],
        "groups": [
            {
                "group": {
                    "name": "group-dev"
                },
                "permission": "PROJECT_WRITE"
            },
            {
                "group": {
                    "name": "group-qa"
                },
                "permission": "PROJECT_READ"
            }
        ],
        "messages": [],
        "project_key": "FOO",
        "users": [
            {
                "permission": "PROJECT_ADMIN",
                "user": {
                    "active": true,
                    "displayName": "admin",
                    "emailAddress": "",
                    "id": 9369,
                    "links": {
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/users/admin"
                            }
                        ]
                    },
                    "name": "admin",
                    "slug": "admin",
                    "type": "NORMAL"
                }
            }
        ]
    }
}

TASK [Retrieve Bitbucket project permissions, only group or user names containing the supplied filter strings will be returned] ***
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "filters": [
            "admin",
            "dev"
        ],
        "groups": [
            {
                "group": {
                    "name": "group-dev"
                },
                "permission": "PROJECT_WRITE"
            }
        ],
        "messages": [],
        "project_key": "FOO",
        "users": []
    }
}
```