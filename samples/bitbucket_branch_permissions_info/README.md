# Overview

This sample shows how to retrieve Bitbucket branch permissions information using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve branch permissions for the supplied repository] **************************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "messages": [],
        "project_key": "FOO",
        "repository": "bar",
        "restrictions": [
            {
                "accessKeys": [],
                "groups": [],
                "id": 4,
                "matcher": {
                    "active": true,
                    "displayId": "develop",
                    "id": "refs/heads/develop",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 187,
                    "type": "REPOSITORY"
                },
                "type": "fast-forward-only",
                "users": [
                    {
                        "active": true,
                        "displayName": "jsmith",
                        "emailAddress": "jsmith@example.com",
                        "id": 5719,
                        "links": {
                            "self": [
                                {
                                    "href": "https://bitbucket.example.com/users/jsmith"
                                }
                            ]
                        },
                        "name": "jsmith",
                        "slug": "jsmith",
                        "type": "NORMAL"
                    }
                ]
            },
            {
                "accessKeys": [],
                "groups": [
                    "bitbucket-admin"
                ],
                "id": 5,
                "matcher": {
                    "active": true,
                    "displayId": "develop",
                    "id": "refs/heads/develop",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 187,
                    "type": "REPOSITORY"
                },
                "type": "pull-request-only",
                "users": []
            }
        ]
    }
}

TASK [Retrieve branch permissions for the supplied project] *****************************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "messages": [],
        "project_key": "FOO",
        "restrictions": [
            {
                "accessKeys": [],
                "groups": [
                    "bitbucket-admins"
                ],
                "id": 9,
                "matcher": {
                    "active": true,
                    "displayId": "Release",
                    "id": "RELEASE",
                    "type": {
                        "id": "MODEL_CATEGORY",
                        "name": "Branching model category"
                    }
                },
                "scope": {
                    "resourceId": 292,
                    "type": "PROJECT"
                },
                "type": "no-deletes",
                "users": []
            }
        ]
    }
}
```