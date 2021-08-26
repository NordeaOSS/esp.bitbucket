.. _bitbucket_branch_info_module:


bitbucket_branch_info -- Retrieve branches information for the supplied project and repository
==============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieve branches information from Bitbucket Server for the supplied project and repository.

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


  branch (False, list, ['*'])
    Retrieve the branches matching the supplied *branch* filter.

    This can be '*' which means all branches.


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

    
    - name: Retrieve all branches
      esp.bitbucket.bitbucket_branch_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no

    - name: Retrieve the branches matching the supplied branch filters
      esp.bitbucket.bitbucket_branch_info:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        repository: bar
        project_key: FOO
        branch: [ develop, feature ]
        validate_certs: no



Return Values
-------------

repository (always, str, bar)
  Bitbucket repository name.


project_key (always, str, FOO)
  Bitbucket project key.


messages (always, list, ['Repository `bar2` does not exist.'])
  List of error messages.


branches (always, list, )
  List of repository branches.


  displayId (success, str, feature/mybranch)
    Branch display ID.


  id (success, str, refs/heads/feature/mybranch)
    Branch ID.


  isDefault (success, bool, False)
    Whether or not the branche is default.


  type (success, str, BRANCH)
    Branch type.


  latestChangeset (success, str, 93b84625d75123b7f7942fd72225400fa66d62ec)
    Latest Changeset id.


  latestCommit (success, str, 93b84625d75123b7f7942fd72225400fa66d62ec)
    Latest Commit id.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

