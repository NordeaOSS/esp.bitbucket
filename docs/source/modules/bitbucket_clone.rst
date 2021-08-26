.. _bitbucket_clone_module:


bitbucket_clone -- Clone a repository from Bitbucket Server
===========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Clones a repository from Bitbucket Server.

Returns the latest commit hash of the cloned repository branch.

Authentication can be done with *token* or with *username* and *password*.






Parameters
----------

  repodir (True, str, None)
    A local destination directory where the repository will be cloned.

    This must be a valid git repository.


  force (False, bool, False)
    Delete a local destination directory before cloning, if it already exists.


  branch (False, str, master)
    A repository branch to clone.


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
   - requirements [ os, pathlib, gitpython ]
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Clone a repository from Bitbucket
      esp.bitbucket.bitbucket_clone:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        branch: master
        path: /tmp/bar  
        force: yes
        validate_certs: no
      register: _result



Return Values
-------------

changed (success, bool, True)
  Whether or not a repository has been cloned from Bitbucket.


json (success, dict, )
  Dictionary with clone details.


  commit_hexsha (success, str, 9074a0e7140e120ae927cb817c0d6fc7ebf6dd37)
    A commit hash of the working tree of the cloned repository branch.






Status
------





Authors
~~~~~~~

- Pawel Smolarz (pawel.smolarz@nordea.com)
- Krzysztof Lewandowski (@klewan)

