.. _bitbucket_webhook_module:


bitbucket_webhook -- Manage repository webhooks on Bitbucket Server
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages repository webhooks on Bitbucket Server.

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


  webhook_name (True, str, wh_<repo>)
    Webhook name to create


  webhook_url (True, str, https://jenkins.example.com/bitbucket-hook/)
    Webhook url


  event (True, str, repo:refs_changed)
    Webhook events list seperated by comma


  state (False, str, present)
    Whether the webhook should exist or not.


  return_content (optional, bool, True)
    Whether or not to return the body of the response as a "content" key in the dictionary result no matter it succeeded or failed.


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

    
    - name: Create webhook
      esp.bitbucket.bitbucket_webhook:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: present
        webhook_name: wh_repo1
        webhook_url: "https://jenkins.example.com/bitbucket-hook/"
        event: "repo:refs_changed"





Status
------





Authors
~~~~~~~

- Pawel Smolarz

