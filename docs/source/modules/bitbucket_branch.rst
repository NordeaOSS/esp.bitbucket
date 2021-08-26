.. _bitbucket_branch_module:


bitbucket_branch -- Manage repository branches on Bitbucket Server
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages repository branches on Bitbucket Server.

It creates a new branch, or sets an existing branch as a default for the supplied repository.

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


  branch (True, str, None)
    Branch name to create or delete


  from_branch (False, str, master)
    New branch will be created from this branch.

    Required when *state=present*.


  state (False, str, present)
    Whether the branch should exist or not. Only creation allowed


  is_default (False, bool, False)
    Set the new branch as default one for the repository.


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

    
    - name: Create branch and set it as default one for the supplied repository
      esp.bitbucket.bitbucket_branch:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: present
        branch: feature/baz
        from_branch: master
        is_default: True
        
    - name: Create branch
      esp.bitbucket.bitbucket_branch:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: present
        branch: feature/baz
        from_branch: master

    - name: Update the default branch of a repository
      esp.bitbucket.bitbucket_branch:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        branch: develop
        is_default: True



Return Values
-------------

project_key (always, str, FOO)
  Bitbucket project key.


repository (always, str, bar)
  Bitbucket repository name.


branch (always, str, develop)
  A specific branch name.


from_branch (success, str, master)
  A source branch name which a new branch is created from.


state (success, str, present)
  Branch state, either *present* or *absent*.


is_default (success, boolean, False)
  Whether or not the branch is set as the default one.


json (success, dict, )
  Details of a new branch.


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
- Pawel Smolarz

