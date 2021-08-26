# Overview

This sample shows how setup default reviewers on Bitbucket repository using ESP Bitbucket Ansible modules.
In this is possible to protect repositories and eg. master branch.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
PLAY [A playbook for bitbucket_repo_reviewer] ********************************************************************************************************************************************************************

TASK [Configure default reviewer on repo level] ******************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_repo_reviewer": {
        "approvals": "0",
        "changed": true,
        "failed": false,
        "json": null,
        "messages": [],
        "project_key": "APITEST",
        "repository": "test04_user1",
        "state": "absent"
    }
}

TASK [Configure default reviewer on repo level] ******************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_repo_reviewer": {
        "approvals": "2",
        "changed": true,
        "failed": false,
        "json": {
            "fetch_url_retries": 1,
            "id": 1042,
            "requiredApprovals": 2,
            "reviewers": [
                {
                    "active": true,
                    "displayName": "Lewandowski, Krzysztof",
                    "emailAddress": "Krzysztof.Lewandowski@nordea.com",
                    "id": 5719,
                    "links": {
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/users/user2"
                            }
                        ]
                    },
                    "name": "user2",
                    "slug": "user2",
                    "type": "NORMAL"
                },
                {
                    "active": true,
                    "displayName": "Smolarz Pawel",
                    "emailAddress": "Pawel.Smolarz@nordea.com",
                    "id": 1942,
                    "links": {
                        "self": [
                            {
                                "href": "https://bitbucket.example.com/users/user1"
                            }
                        ]
                    },
                    "name": "user1",
                    "slug": "user1",
                    "type": "NORMAL"
                }
            ],
            "scope": {
                "resourceId": 406,
                "type": "REPOSITORY"
            },
            "sourceRefMatcher": {
                "active": true,
                "displayId": "refs/heads/**",
                "id": "refs/heads/**",
                "type": {
                    "id": "PATTERN",
                    "name": "Pattern"
                }
            },
            "targetRefMatcher": {
                "active": true,
                "displayId": "master",
                "id": "refs/heads/master",
                "type": {
                    "id": "BRANCH",
                    "name": "Branch"
                }
            }
        },
        "messages": [],
        "project_key": "APITEST",
        "repository": "test04_user1",
        "state": "present"
    }
}

PLAY RECAP *******************************************************************************************************************************************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```