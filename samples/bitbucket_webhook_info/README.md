# Overview

This sample shows how get information about webhooks on Bitbucket repository using ESP Bitbucket Ansible modules.

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

TASK [Get webhooks info] *****************************************************************************************************************************************************************************************
ok: [localhost]

TASK [debug] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "ebi_create_output": {
        "changed": false,
        "failed": false,
        "json": [
            {
                "active": true,
                "configuration": {},
                "createdDate": 1618233794469,
                "events": [
                    "repo:refs_changed"
                ],
                "id": 40,
                "name": "wh_jenkins2",
                "updatedDate": 1618233794469,
                "url": "https://jenkins.example.com/bitbucket-hook/"
            },
            {
                "active": true,
                "configuration": {},
                "createdDate": 1618233794470,
                "events": [
                    "repo:modified"
                ],
                "id": 41,
                "name": "wh_jenkins",
                "updatedDate": 1618233794470,
                "url": "https://jenkins.example.com/bitbucket-hook/"
            }
        ],
        "messages": [],
        "project_key": "APITEST",
        "repository": "test04_user1",
        "state": "present"
    }
}

```