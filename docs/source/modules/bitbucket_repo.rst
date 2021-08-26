.. _bitbucket_repo_module:


bitbucket_repo -- Manage your repositories on Bitbucket Server
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages Bitbucket Server repositories.

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


  state (False, str, present)
    Whether the repository should exist or not.


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

    
    - name: Create repository
      esp.bitbucket.bitbucket_repo:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: present

    - name: Create repository using token
      esp.bitbucket.bitbucket_repo:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        name: bar
        project: FOO
        validate_certs: no
        state: present

    - name: Delete repository
      esp.bitbucket.bitbucket_repo:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        validate_certs: no
        state: absent



Return Values
-------------

name (success, str, bar)
  Bitbucket repository name (if *state=present*).


project (success, dict, )
  Information about Bitbucket project (if *state=present*).


  id (success, int, 200)
    Project ID.


  key (success, str, FOO)
    Bitbucket project key.


  name (success, str, FOO project)
    Bitbucket project name.


  public (success, bool, False)
    Whether or not the project is public.


  type (success, str, NORMAL)
    Bitbucket project type.


  self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO'}])
    Links to Bitbucket project.



links (success, dict, )
  Links to Bitbucket repository (if *state=present*).


  clone (success, list, [{'href': 'https://bitbucket.example.com/scm/foo/bar.git', 'name': 'http'}, {'href': 'ssh://git@bitbucket.example.com:7999/foo/bar.git', 'name': 'ssh'}])
    Clone URLs.


  self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO/repos/bar/browse'}])
    Links to Bitbucket repository.



forkable (success, bool, True)
  Source file used for the copy on the target machine (if *state=present*).


hierarchyId (success, str, 91369a5b9598e936d126)
  Hierarchy ID (if *state=present*).


id (success, int, 100)
  Repository ID (if *state=present*).


public (success, bool, True)
  Whether or not the repository is public (if *state=present*).


scmId (success, str, git)
  SCM type (if *state=present*).


slug (success, str, bar)
  Bitbucket repository slug name (if *state=present*).


state (success, str, AVAILABLE)
  Bitbucket repository state, after execution (if *state=present*).


statusMessage (success, str, Available)
  Bitbucket repository state message, after execution (if *state=present*).


context (success, str, None)
  Context (if *state=absent*).


exceptionName (success, str, None)
  Exception Name (if *state=absent*).


message (success, str, Repository scheduled for deletion.)
  Deletion message (if *state=absent*).





Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)
- Evgeniy Krysanov (@catcombo)

