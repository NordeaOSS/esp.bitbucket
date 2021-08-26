.. _bitbucket_project_permissions_module:


bitbucket_project_permissions -- Manage Bitbucket project permissions
=====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Promote or demote a group's or a users's permission level for the specified project.

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


  user (False, str, None)
    Bitbucket user to grant or revoke permission from.

    This is only needed when not using *group*.


  group (False, str, None)
    Bitbucket group to grant or revoke permission from.

    This is only needed when not using *user*.


  permission (True, str, None)
    The permission to grant.

    Empty string '' means revoke all grants form a user or group.


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

    
    - name: Set PROJECT_WRITE permission level for the specified project to jsmith user
      esp.bitbucket.bitbucket_project_permissions:
        url: 'https://bitbucket.example.com'
        username: admin
        password: secrect
        project_key: FOO
        user: jsmith
        permission: PROJECT_WRITE
        validate_certs: no

    - name: Revoke all permissions for the specified project from a group
      esp.bitbucket.bitbucket_project_permissions:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        project_key: FOO
        group: dev-group
        permission: ''
        validate_certs: no



Return Values
-------------

project_key (always, str, FOO)
  Bitbucket project key.


permission (always, str, PROJECT_WRITE)
  The permission to grant. Empty string '' means revoke all grants form a user or group.


user (success, str, jsmith)
  Bitbucket user to grant or revoke permission from.


group (success, str, dev-group)
  Bitbucket group to grant or revoke permission from.





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

