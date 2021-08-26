.. _bitbucket_branch_permissions_info_module:


bitbucket_branch_permissions_info -- Retrieve branch permissions
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Search for branch restrictions for the supplied project or repository.

A restriction means preventing writes on the specified branch by all except a set of users and/or groups, or preventing specific operations such as branch deletion.

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


  project_key (True, str, None)
    Bitbucket project key.


  repository (False, str, None)
    Repository name.


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

    
    - name: Retrieve branch permissions for the supplied project
      esp.bitbucket.bitbucket_branch_permissions_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: FOO
        validate_certs: no

    - name: Retrieve branch permissions for the supplied repository
      esp.bitbucket.bitbucket_branch_permissions_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: FOO
        repository: bar
        validate_certs: no



Return Values
-------------

messages (always, list, ['Project `FOOO` does not exist.'])
  List of error messages.


project_key (always, str, FOO)
  Bitbucket project key.


repository (success, str, bar)
  Bitbucket repository name.


restrictions (always, list, )
  List of branch restrictions for the supplied project or repository.


  matcher (success, dict, {'active': True, 'displayId': 'Release', 'id': 'RELEASE', 'type': {'id': 'MODEL_CATEGORY', 'name': 'Branching model category'}})
    Matcher description.


  scope (success, dict, {'resourceId': 292, 'type': 'PROJECT'})
    Scope.


  groups (success, list, ['bitbucket-admin'])
    Bitbucket groups.


  users (success, list, ['joe', 'jsmith'])
    Bitbucket users.


  accessKeys (success, list, [])
    Bitbucket access keys.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

