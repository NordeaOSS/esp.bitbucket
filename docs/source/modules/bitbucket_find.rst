.. _bitbucket_find_module:


bitbucket_find -- Retrieve a list of files from particular repository of a Bitbucket Server based on specific criteria
======================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieve a list of matching file names from particular repository of a Bitbucket Server.

Files are selected based on ``patterns`` option. Additionaly, files can be further filtered out by ``grep`` option to select only those matching the supplied grep pattern.

Combined outcome of ``patterns`` and ``grep`` options form the final list of files returned by this module.

The search is done using Python regex patterns.

Authentication can be done with *token* or with *username* and *password*.






Parameters
----------

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


  at (False, str, None)
    The commit ID or ref (e.g. a branch or tag) to read a file at.

    If not specified the default branch will be used instead.


  patterns (optional, list, [])
    List of Python regex patterns to search for in file names on a Bitbucket Server repository.

    The patterns restrict the list of files to be returned to those whose basenames match at least one of the patterns specified. Multiple patterns can be specified using a list.

    This parameter expects a list, which can be either comma separated or YAML. If any of the patterns contain a comma, make sure to put them in a list to avoid splitting the patterns in undesirable ways.

    Defaults to '.+'.


  grep (False, str, None)
    Python regex pattern to search for in each file selected from repository to form the final list of files.

    Files are selected based on ``patterns`` option.

    Combined outcome of ``patterns`` and ``grep`` options form the final list of files returned by this module.

    If not specified, search will not be executed.


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
   - Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
   - Supports ``check_mode``.


See Also
--------

.. seealso::



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Retrieve paths of all files in a repository at develop branch
      esp.bitbucket.bitbucket_find:
        url: 'https://bitbucket.example.com'
        username: '{{ bitbucket_username }}'
        password: '{{ bitbucket_password }}'
        repository: bar
        project_key: FOO
        at: develop
        validate_certs: no

    - name: Retrieve paths of all files in a repository that end specific way
      esp.bitbucket.bitbucket_find:
        url: 'https://bitbucket.example.com'
        username: '{{ bitbucket_username }}'
        password: '{{ bitbucket_password }}'
        repository: bar
        project_key: FOO
        patterns:
          - '.+\.yml$'
          - '.+\.json$'
        validate_certs: no

    - name: Retrieve paths of all files with 'baz' in their names in develop branch and with the supplied grep pattern in the files content
      esp.bitbucket.bitbucket_find:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        repository: bar
        project_key: FOO
        patterns: baz
        at: develop
        grep: 'hello.+?world'    
        validate_certs: no



Return Values
-------------

repository (always, str, bar)
  Bitbucket repository name.


project_key (always, str, FOO)
  Bitbucket project key.


messages (always, list, ['Repository `bar2` does not exist.'])
  List of error messages.


at (always, str, master)
  The commit ID or ref (e.g. a branch or tag) to read a file at.


patterns (always, list, ['.+\\.yml$', '.+\\.json$'])
  List of Python regex patterns to search for in file names on a Bitbucket Server repository.


grep (always, str, hello)
  Python regex pattern to search for in each file selected from repository to form the final list of files.


files (success, list, ['path/to/baz.yml', 'path/to/vault.yml'])
  List of matching file names from particular repository.





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

