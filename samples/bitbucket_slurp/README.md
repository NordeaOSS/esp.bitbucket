# Overview

This sample shows how to read a file from Bitbucket Server and expose it in a base64-encoded blob containing the file data.

It uses `esp.bitbucket.bitbucket_slurp` module to fetch the file content.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Read file contents from Bitbucket Server] **********************************************************
ok: [localhost]

TASK [debug] *********************************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": false,
        "content": "LS0tCmhlbGxvOiB3b3JsZAoK",
        "encoding": "base64",
        "failed": false,
        "fetch_url_retries": 1,
        "url": "https://bitbucket.example.com/rest/api/1.0/projects/FOO/repos/bar/raw/path/to/baz.yml"
    }
}

TASK [debug] *********************************************************************************************
ok: [localhost] => {
    "msg": "---\nhello: world\n\n"
}

TASK [debug] *********************************************************************************************
ok: [localhost] => {
    "msg": {
        "hello": "world"
    }
}
```