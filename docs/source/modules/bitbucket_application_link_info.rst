.. _bitbucket_application_link_info_module:


bitbucket_application_link_info -- Retrieve application links
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Search for application links on Bitbucket Server.

One may refer to an application link either by its ID or its name.

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


  applink (False, list, ['*'])
    Retrieve application links matching the supplied *applink* filter.

    This can be '*' which means all application links.

    One may refer to an application link either by its ID or its name.


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

    
    - name: Retrieve details on the given application links (supplied by names or IDs)
      esp.bitbucket.bitbucket_application_link_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        applink:
          - FOO
          - 227dd1d7-f6d6-34a5-b046-5663fb518691
        validate_certs: no

    - name: Retrieve details on all application links
      esp.bitbucket.bitbucket_application_link_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        applink:
          - '*'
        validate_certs: no



Return Values
-------------

applicaton_links (always, list, [{'data': {}, 'displayUrl': 'https://terraform.example.com/my-org', 'id': '227dd1d7-f6d6-34a5-b046-5663fb518691', 'name': 'Terraform (my-org)', 'primary': False, 'properties': {}, 'rpcUrl': 'https://terraform.example.com/app/my-org', 'system': False, 'type': 'generic'}])
  List of application links data.





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

