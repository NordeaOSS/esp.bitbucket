.. _bitbucket_pull_request_module:


bitbucket_pull_request -- Manage repository pull requests on Bitbucket Server
=============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages repository pull requests on Bitbucket Server.

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


  title (False, str, None)
    Title for pull request


  from_branch (True, str, develop)
    Source branch for pull request


  to_branch (True, str, master)
    Destination branch for pull request


  reviewers (False, list, None)
    List of pull request reviewers


  state (False, str, present)
    Whether the pull should exist or not.


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

    
    - name: Create pull request
      esp.bitbucket.bitbucket_pull_request:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: present
        title: "Pull request from develop to master branch"
        from_branch: "develop"
        to_branch: "master"
        reviewers: [ m00001, m00002 ]
        
    - name: Delete pull request on repository
      esp.bitbucket.bitbucket_pull_request:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: absent
        from_branch: "develop"
        to_branch: "master"





Status
------





Authors
~~~~~~~

- Pawel Smolarz

