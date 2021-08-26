.. _bitbucket_pull_request_info_module:


bitbucket_pull_request_info -- Get information about pull requests on Bitbucket Server
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get information about pull requests on Bitbucket Server.

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

    
    - name: Get information about pull requests
      esp.bitbucket.bitbucket_pull_request_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no



Return Values
-------------

messages (always, list, ['Project `FOOO` does not exist.'])
  List of error messages.


project_key (success, str, FOO)
  Bitbucket project key.


repository (success, str, bar)
  Bitbucket repository name.


json (success, list, )
  List of pull requests for the supplied project and repository.


  author (success, str, john)
    Pull request author.


  title (success, str, baz.yml edited online with Bitbucket)
    Pull request title.


  fromRef (success, str, develop)
    From branch name.


  toRef (success, str, master)
    To branch name.


  id (success, int, 2)
    Pull request id.


  version (success, int, 0)
    Pull request version.


  reviewers (success, list, ['joe', 'jsmith'])
    List of reviewers.






Status
------





Authors
~~~~~~~

- Pawel Smolarz

