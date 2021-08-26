# Overview

This sample shows how create pull requests on Bitbucket repository using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
PLAY [A playbook for ansible_bitbucket_project project] **********************************************************************************************************************************************************

TASK [Create pull request on repository] *************************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_pull_output": {
        "changed": true,
        "failed": false,
        "json": {
            "author": {
                "approved": false,
                "role": "AUTHOR",
                "status": "UNAPPROVED",
                "user": {
                    "active": true,
                    "displayName": "Smolarz Pawel",
                    "emailAddress": "Pawel.Smolarz@nordea.com",
                    "id": 1942,
                    "links": {
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/users/user_id"
                            }
                        ]
                    },
                    "name": "user_id",
                    "slug": "user_id",
                    "type": "NORMAL"
                }
            },
            "closed": false,
            "createdDate": 1618317003681,
            "description": "Test pull",
            "fetch_url_retries": 1,
            "fromRef": {
                "displayId": "pull_test",
                "id": "refs/heads/pull_test",
                "latestCommit": "22d1f744d0481cc247a33e1e1552210f923b9d39",
                "repository": {
                    "forkable": true,
                    "hierarchyId": "f65bb740d5b37905c2a0",
                    "id": 251,
                    "links": {
                        "clone": [
                            {
                                "href": "ssh://git@bitbucket.example.com:34002/repo/repo01.git",
                                "name": "ssh"
                            },
                            {
                                "href": "https://bitbucket.example.com/scm/repo/repo01.git",
                                "name": "http"
                            }
                        ],
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/projects/repo/repos/repo01/browse"
                            }
                        ]
                    },
                    "name": "repo01",
                    "project": {
                        "id": 262,
                        "key": "project",
                        "links": {
                            "self": [
                                {
                                    "href": "https://bitbucket.example.com/projects/project"
                                }
                            ]
                        },
                        "name": "project",
                        "public": false,
                        "type": "NORMAL"
                    },
                    "public": false,
                    "scmId": "git",
                    "slug": "repo01",
                    "state": "AVAILABLE",
                    "statusMessage": "Available"
                }
            },
            "id": 17,
            "links": {
                "self": [
                    {
                        "href": "https://bitbucket.example.com/projects/repo/repos/repo01/pull-requests/17"
                    }
                ]
            },
            "locked": false,
            "open": true,
            "participants": [],
            "reviewers": [],
            "state": "OPEN",
            "title": "Test pull",
            "toRef": {
                "displayId": "master",
                "id": "refs/heads/master",
                "latestCommit": "ee45e83fef8396966f34d67c390025b0f749a932",
                "repository": {
                    "forkable": true,
                    "hierarchyId": "f65bb740d5b37905c2a0",
                    "id": 251,
                    "links": {
                        "clone": [
                            {
                                "href": "ssh://git@bitbucket.example.com:34002/repo/repo01.git",
                                "name": "ssh"
                            },
                            {
                                "href": "https://bitbucket.example.com/scm/repo/repo01.git",
                                "name": "http"
                            }
                        ],
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/projects/repo/repos/repo01/browse"
                            }
                        ]
                    },
                    "name": "repo01",
                    "project": {
                        "id": 262,
                        "key": "project",
                        "links": {
                            "self": [
                                {
                                    "href": "https://bitbucket.example.com/projects/project"
                                }
                            ]
                        },
                        "name": "project",
                        "public": false,
                        "type": "NORMAL"
                    },
                    "public": false,
                    "scmId": "git",
                    "slug": "repo01",
                    "state": "AVAILABLE",
                    "statusMessage": "Available"
                }
            },
            "updatedDate": 1618317003681,
            "version": 0
        },
        "messages": [],
        "project_key": "project",
        "repository": "repo01",
        "state": "present"
    }
}

TASK [Get pull requests on repository] ***************************************************************************************************************************************************************************
ok: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_pull_info_output": {
        "changed": false,
        "failed": false,
        "json": [
            {
                "author": "user_id",
                "fromRef": "pull_test",
                "pull_id": 17,
                "title": "Test pull",
                "toRef": "master",
                "version": 0
            },
            {
                "author": "user_id",
                "fromRef": "pull_test2",
                "pull_id": 16,
                "title": "develop",
                "toRef": "master",
                "version": 0
            }
        ],
        "messages": [],
        "project_key": "project",
        "repository": "repo01"
    }
}

```