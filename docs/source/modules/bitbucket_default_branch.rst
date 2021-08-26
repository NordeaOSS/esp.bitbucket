.. _bitbucket_default_branch_module:


bitbucket_default_branch -- Update the default branch of a repository
=====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set the default branch of a repository.

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


  branch (True, str, develop)
    Branch name to set as default


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

    
    - name: Update the default branch of a repository
      esp.bitbucket.bitbucket_default_branch:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        branch: develop



Return Values
-------------

project_key (always, str, FOO)
  Bitbucket project key.


repository (always, str, bar)
  Bitbucket repository name.


branch (always, str, master)
  Branch name to set as default.


isDefault (success, bool, True)
  Whether the branch is a default branch for the supplied repository.





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski
- Pawel Smolarz

