# Overview

This sample shows how to manage Bitbucket branch permissions using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Create restrictions for the supplied branch] **************************************
changed: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "branch_name": "master",
        "changed": true,
        "failed": false,
        "messages": [],
        "project_key": "FOO",
        "repository": "bar",
        "restrictions": [
            {
                "exemptions": {
                    "access_keys": [],
                    "groups": [],
                    "users": [
                        "john"
                    ]
                },
                "prevent": "deletion"
            },
            {
                "exemptions": {
                    "access_keys": [],
                    "groups": [],
                    "users": []
                },
                "prevent": "rewriting history"
            },
            {
                "exemptions": {
                    "access_keys": [],
                    "groups": [],
                    "users": []
                },
                "prevent": "changes without a pull request"
            },
            {
                "exemptions": {
                    "access_keys": [],
                    "groups": [],
                    "users": []
                },
                "prevent": "all changes"
            }
        ],
        "results": [
            {
                "accessKeys": [],
                "fetch_url_retries": 1,
                "groups": [],
                "id": 52,
                "matcher": {
                    "active": true,
                    "displayId": "master",
                    "id": "refs/heads/master",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 268,
                    "type": "REPOSITORY"
                },
                "type": "no-deletes",
                "users": [
                    {
                        "active": true,
                        "id": 5719,
                        "links": {
                            "self": [
                                {
                                    "href": "https://bitbucket.example.co/users/john"
                                }
                            ]
                        },
                        "name": "john",
                        "slug": "john",
                        "type": "NORMAL"
                    }
                ]
            },
            {
                "accessKeys": [],
                "fetch_url_retries": 1,
                "groups": [],
                "id": 53,
                "matcher": {
                    "active": true,
                    "displayId": "master",
                    "id": "refs/heads/master",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 268,
                    "type": "REPOSITORY"
                },
                "type": "fast-forward-only",
                "users": []
            },
            {
                "accessKeys": [],
                "fetch_url_retries": 1,
                "groups": [],
                "id": 54,
                "matcher": {
                    "active": true,
                    "displayId": "master",
                    "id": "refs/heads/master",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 268,
                    "type": "REPOSITORY"
                },
                "type": "pull-request-only",
                "users": []
            },
            {
                "accessKeys": [],
                "fetch_url_retries": 1,
                "groups": [],
                "id": 55,
                "matcher": {
                    "active": true,
                    "displayId": "master",
                    "id": "refs/heads/master",
                    "type": {
                        "id": "BRANCH",
                        "name": "Branch"
                    }
                },
                "scope": {
                    "resourceId": 268,
                    "type": "REPOSITORY"
                },
                "type": "read-only",
                "users": []
            }
        ],
        "state": "present"
    }
}
```