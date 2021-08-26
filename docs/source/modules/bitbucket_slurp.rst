.. _bitbucket_slurp_module:


bitbucket_slurp -- Slurps a file from Bitbucket Server
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module is used for fetching a base64-encoded blob containing the data in a file on Bitbucket Server.

Authentication can be done with *token* or with *username* and *password*.






Parameters
----------

  src (True, path, None)
    The file on the Bitbucket Server to fetch. This *must* be a file, not a directory.


  at (False, str, None)
    The commit ID or ref (e.g. a branch or tag) to read a file at.

    If not specified the default branch will be used instead.


  url (False, str, None)
    Bitbucket Server URL.


  username (False, str, None)
    Username used for authentication.

    This is only needed when not using *token*.

    Required when *password* is provided.


  password (False, str, None)
    Password used for authentication.

    This is only needed when not using *token*.

    Required when *username* is provided.


  token (False, str, None)
    Token parameter for authentication.

    This is only needed when not using *username* and *password*.


  repository (True, str, None)
    Repository name.


  project_key (True, str, None)
    Bitbucket project key.


  validate_certs (optional, bool, True)
    If ``no``, SSL certificates will not be validated.

    This should only set to ``no`` used on personally controlled sites using self-signed certificates.


  use_proxy (optional, bool, True)
    If ``no``, it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  sleep (optional, int, 5)
    Number of seconds to sleep between API retries.


  retries (optional, int, 3)
    Number of retries to call Bitbucket API URL before failure.





Notes
-----

.. note::
   - This module returns an 'in memory' base64 encoded version of the file, take into account that this will require at least twice the RAM as the original file size.
   - Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Read baz.yml file contents from Bitbucket Server from default branch
      esp.bitbucket.bitbucket_slurp:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        src: 'path/to/baz.yml'
        validate_certs: no
        force_basic_auth: yes
      register: _result

    - name: Print returned information
      ansible.builtin.debug:
        msg: "{{ _result['content'] | b64decode }}"

    - name: Read baz.yml file contents from Bitbucket Server from develop branch
      esp.bitbucket.bitbucket_slurp:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        repository: bar
        project_key: FOO
        src: 'path/to/baz.yml'
        at: develop
        validate_certs: no
      register: _result



Return Values
-------------

content (success, str, LS0tCmhlbGxvOiB3b3JsZAoK)
  Encoded file content


encoding (success, str, base64)
  Type of encoding used for file


url (success, str, https://bitbucket.example.com/rest/api/1.0/projects/FOO/repos/bar/raw/path/to/baz.yml)
  Actual URL of file slurped





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

