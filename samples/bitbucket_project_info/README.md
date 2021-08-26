# Overview

This sample shows how to retrieve Bitbucket projects information using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve all projects] ************************************************************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "filter": [
            "*"
        ],
        "messages": [],
        "projects": [
            {
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
            {
                "description": "This is a new Bitbucket project",
                "id": 308,
                "key": "FOO2",
                "links": {
                    "self": [
                        {
                            "href": "https://bitbucket.example.com/projects/FOO2"
                        }
                    ]
                },
                "name": "A new Bitbucket project2",
                "public": false,
                "type": "NORMAL"
            }
        ]
    }
}

TASK [Retrieve the projects matching the supplied project_key filter] *******************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "filter": [
            "FOO",
            "BAR"
        ],
        "messages": [
            "Project `BAR` does not exist."
        ],
        "projects": [
            {
                "description": "This is a new Bitbucket project",
                "fetch_url_retries": 1,
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
        ]
    }
}
```