.. _bitbucket_copy_module:


bitbucket_copy -- Copy files to Bitbucket Server
================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``bitbucket_copy`` module copies (pushes) a file from the local machine to a Bitbucket Server repository.

Creates the file if it does not exist.

Authentication can be done with *token* or with *username* and *password*.






Parameters
----------

  src (False, path, None)
    Local path to a file to copy to the Bitbucket Server repository.

    This can be absolute or relative.

    Required when content is not provided.


  content (False, str, None)
    When used instead of ``src``, sets the contents of a file directly to the specified value.

    Required when src is not provided.


  dest (True, path, None)
    Path in Bitbucket repositorywhere the file should be copied to.


  message (False, str, None)
    Commit message.

    If not specified the default message should be used.


  branch (False, str, None)
    The branch to write a file at.

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
   - Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Copy file to Bitbucket
      esp.bitbucket.bitbucket_copy:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        src: /tmp/baz.yml
        dest: path/to/baz.yml
        message: File updated using bitbucket_copy module
        branch: master
        validate_certs: no
        force_basic_auth: yes

    - name: Copy file to Bitbucket using inline content
      esp.bitbucket.bitbucket_copy:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        content: '# Hello world'
        dest: path/to/baz.yml
        message: File updated using bitbucket_copy module
        branch: master
        validate_certs: no
        force_basic_auth: yes



Return Values
-------------

repository (always, str, bar)
  Bitbucket repository name.


project_key (always, str, FOO)
  Bitbucket project key.


branch (always, str, master)
  Branch name.


dest (always, str, path/to/baz.yml)
  Path in Bitbucket repositorywhere the file was copied to.


src (success, str, /tmp/baz.yml)
  Local path to a file which was copied to the Bitbucket Server repository.


json (success, dict, )
  Dictionary with updated file details.


  author (success, dict, {'active': True, 'displayName': 'John Smith', 'emailAddress': 'john.smith@example.com', 'id': 5719, 'links': {'self': [{'href': 'https://bitbucket.example.com/users/jsmith'}]}, 'name': 'jsmith', 'slug': 'jsmith', 'type': 'NORMAL'})
    Commit request author.


  committer (success, dict, {'active': True, 'displayName': 'John Smith', 'emailAddress': 'john.smith@example.com', 'id': 5719, 'links': {'self': [{'href': 'https://bitbucket.example.com/users/jsmith'}]}, 'name': 'jsmith', 'slug': 'jsmith', 'type': 'NORMAL'})
    Committer.


  authorTimestamp (success, int, 1618819213000)
    Timestamp.


  committerTimestamp (success, int, 1618819213000)
    Timestamp.


  message (success, str, File updated using bitbucket_copy module)
    Commit message.


  id (success, str, 2525b8cc320c6c5c71a84d1c21f0554b012214df)
    Commit id.


  displayId (success, str, 2525b8cc320)
    Commit id.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

