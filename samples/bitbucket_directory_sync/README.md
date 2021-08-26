# Overview

This sample shows how to synchronise Bitbucket Server User Directories, e.g. synchronise users and groups with Active Directory.

It uses `esp.bitbucket.bitbucket_directory_sync` module to get user directories synchronized.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [Synchronise User Directories] ***********************************************************************************
changed: [localhost]

TASK [debug] **********************************************************************************************************
ok: [localhost] => {
    "_result": {
        "changed": true,
        "failed": false,
        "user_directories_synced": [
            {
                "directoryId": 262145,
                "info": {
                    "cache-control": "private",
                    "connection": "keep-alive",
                    "content-language": "en-US",
                    "content-type": "text/html;charset=UTF-8",
                    "cookies": {},
                    "cookies_string": "",
                    "date": "Wed, 07 Apr 2021 11:37:45 GMT",
                    "expires": "Thu, 01 Jan 1970 00:00:00 GMT",
                    "keep-alive": "timeout=20",
                    "msg": "OK (unknown bytes)",
                    "status": 200,
                    "transfer-encoding": "chunked",
                    "url": "https://bitbucket.example.com/plugins/servlet/embedded-crowd/directories/list?highlightDirectoryId=262145&xsrfTokenName=atl_token&xsrfTokenValue=a403f6650183da7ea43c2ce8b0a144efb43e062f",
                    "vary": "accept-encoding",
                    "x-content-type-options": "nosniff",
                    "x-frame-options": "SAMEORIGIN",
                    "x-xss-protection": "1; mode=block"
                },
                "operation": "/plugins/servlet/embedded-crowd/directories/sync?directoryId=262145&atl_token=a403f6650183da7ea43c2ce8b0a144efb43e062f"
            }
        ]
    }
}
```