# Overview

This sample shows how to retrieve Bitbucket repositories information using ESP Bitbucket Ansible modules.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Retrieve all repositories] ********************************************************
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
        "project_key": "FOO",
        "repositories": [
            {
                "forkable": true,
                "hierarchyId": "b47b96c575381ef749b2",
                "id": 187,
                "links": {
                    "clone": [
                        {
                            "href": "https://bitbucket.example.com/scm/foo/bar.git",
                            "name": "http"
                        },
                        {
                            "href": "ssh://git@bitbucket.example.com:34002/foo/bar.git",
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
        ]
    }
}

TASK [Retrieve the repositories matching the supplied repository filter] ****************
ok: [localhost]

TASK [debug] ****************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "failed": false,
        "filter": [
            "bar",
            "baz"
        ],
        "messages": [
            "Repository `baz` does not exist."
        ],
        "project_key": "FOO",
        "repositories": [
            {
                "fetch_url_retries": 1,
                "forkable": true,
                "hierarchyId": "b47b96c575381ef749b2",
                "id": 187,
                "links": {
                    "clone": [
                        {
                            "href": "https://bitbucket.example.com/scm/foo/bar.git",
                            "name": "http"
                        },
                        {
                            "href": "ssh://git@bitbucket.example.com:34002/foo/bar.git",
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
        ]
    }
}
```