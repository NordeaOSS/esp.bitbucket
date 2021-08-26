# Overview

This sample shows how to read a file from Bitbucket Server and expose it in a base64-encoded blob containing the file data.

It uses `esp.bitbucket.bitbucket_file` lookup to fetch the file content.

<br>

# Instructions

To run the sample, simply run `sample.yml` playbook:

```bash
ansible-playbook sample.yml
```

<br>

### Ansible playbook output:

```
TASK [lookup | Read file contents from Bitbucket Server] ************************
ok: [localhost] => {
    "msg": {
        "hello": "world"
    }
}

TASK [lookup | Display multiple file contents] **********************************
ok: [localhost] => (item=[Processing a file from Bitbucket Server ..]) => {
    "msg": "---\nhello: world\n\n"
}
ok: [localhost] => (item=[Processing a file from Bitbucket Server ..]) => {
    "msg": "abc\n\n"
}

TASK [lookup | Read vaulted file, do not decrypt it] ****************************
ok: [localhost] => {
    "msg": "$ANSIBLE_VAULT;1.1;AES256 34393536303033366233303662643438313037346566636430386462656135306537366561643630 6364653766303233626364316236653832383465656630380a303462663238393330633336346532 36353135363665333130343264303535386635653431323463643239666565336236633864316130 6263356438313733340a396336376634386431666432366438643266386362643762313665656565 33383137383235326438356661626439356466326666383762353933353639613639"
}

TASK [lookup | Read vaulted file, decrypt it] ***********************************
ok: [localhost] => {
    "msg": {
        "secret_var": true
    }
}
```