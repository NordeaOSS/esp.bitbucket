.. _bitbucket_repo_permissions_info_module:


bitbucket_repo_permissions_info -- Retrieve Bitbucket repository permissions information
========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieve a list of groups and users that have been granted at least one permission for the specified repository.

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


  repository (True, str, None)
    Repository name.


  filters (False, list, ['*'])
    If specified, only group or user names containing the supplied filter strings will be returned.

    This can be '*' which means all groups and users.

    Filters are concatenated with OR operator.


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

    
    - name: Retrieve Bitbucket repository permissions information
      esp.bitbucket.bitbucket_repo_permissions_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: FOO
        repository: bar
        validate_certs: no

    - name: Retrieve Bitbucket repository permissions, only group or user names containing the supplied filter strings will be returned
      esp.bitbucket.bitbucket_repo_permissions_info:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        project_key: FOO
        repository: bar
        filters: [ admin, read ]
        validate_certs: no



Return Values
-------------

messages (always, list, ['Project `FOOO` does not exist.'])
  List of error messages.


project_key (always, str, FOO)
  Bitbucket project key.


repository (always, str, bar)
  Bitbucket repository name.


groups (always, list, )
  List of Bitbucket groups that have been granted at least one permission for the specified repository.


  group (success, dict, )
    Bitbucket group details.


    name (success, str, group-read)
      Bitbucket group name.



  permission (success, str, REPO_READ)
    Bitbucket permission name.



users (always, list, )
  List of Bitbucket users that have been granted at least one permission for the specified repository.


  user (success, dict, )
    Bitbucket user details.


    name (success, str, admin)
      Bitbucket user name.


    type (success, str, NORMAL)
      Bitbucket user type.


    slug (success, str, admin)
      Bitbucket user slug.


    active (success, bool, True)
      Bitbucket user active status.


    displayName (success, str, admin)
      Bitbucket user displayName.


    id (success, int, 9000)
      Bitbucket user id.



  permission (success, str, REPO_WRITE)
    Bitbucket permission name.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

