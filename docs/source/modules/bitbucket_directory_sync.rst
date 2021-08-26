.. _bitbucket_directory_sync_module:


bitbucket_directory_sync -- Synchronise User Directories on Bitbucket Server
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Synchronises User Directories on Bitbucket Server.

Authentication should be done with *username* and *password*.






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
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Synchronise User Directories
      esp.bitbucket.bitbucket_directory_sync:
        url: 'https://bitbucket.example.com'
        username: admin
        password: secrect
        validate_certs: no



Return Values
-------------

user_directories_synced (success, list, )
  List of synchronised User Directories.


  directoryId (success, int, 262145)
    Directory ID.


  operation (success, str, /plugins/servlet/embedded-crowd/directories/sync?directoryId=262145&atl_token=4731c4d872b4b4cf6e2d46a75061213d414a1af7)
    Sync operation URL path.


  info (success, dict, {'status': 200, 'msg': 'OK (unknown bytes)'})
    Bitbucket API response info.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

