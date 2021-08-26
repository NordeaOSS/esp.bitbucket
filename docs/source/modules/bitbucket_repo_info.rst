.. _bitbucket_repo_info_module:


bitbucket_repo_info -- Retrieve repositories information for the supplied project
=================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieve repositories information from Bitbucket Server for the supplied project.

Only repositories for which the authenticated user has the REPO_READ permission will be returned.

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


  repository (False, list, ['*'])
    Retrieve repositories matching the supplied *repository* filter.

    This can be '*' which means all repositories.


  project_key (True, str, None)
    Bitbucket project key.


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

    
    - name: Retrieve all repositories
      esp.bitbucket.bitbucket_repo_info:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: [ '*' ]
        project_key: FOO
        validate_certs: no

    - name: Retrieve the repositories matching the supplied repository filter
      esp.bitbucket.bitbucket_repo_info:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        repository: [ bar, baz ]
        project_key: FOO
        validate_certs: no



Return Values
-------------

project_key (always, str, FOO)
  Bitbucket project key.


messages (always, list, ['Repository `baz` does not exist.'])
  List of error messages.


repositories (always, list, )
  List of repositories.


  forkable (success, bool, True)
    Source file used for the copy on the target machine.


  hierarchyId (success, str, 91369a5b9598e936d126)
    Hierarchy ID.


  id (success, int, 100)
    Repository ID.


  public (success, bool, True)
    Whether or not the repository is public.


  scmId (success, str, git)
    SCM type.


  slug (success, str, bar)
    Bitbucket repository slug name.


  name (success, str, bar)
    Bitbucket repository name.


  state (success, str, AVAILABLE)
    Bitbucket repository state, after execution.


  statusMessage (success, str, Available)
    Bitbucket repository state message, after execution.


  links (success, dict, )
    Links to Bitbucket repository.


    clone (success, list, [{'href': 'https://bitbucket.example.com/scm/foo/bar.git', 'name': 'http'}, {'href': 'ssh://git@bitbucket.example.com:7999/foo/bar.git', 'name': 'ssh'}])
      Clone URLs.


    self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO/repos/bar/browse'}])
      Links to Bitbucket repository.



  project (success, dict, )
    Information about Bitbucket project.


    id (success, int, 200)
      Project ID.


    key (success, str, FOO)
      Bitbucket project key.


    name (success, str, FOO project)
      Bitbucket project name.


    description (success, str, This is a Bitbucket project)
      Bitbucket project description.


    public (success, bool, False)
      Whether or not the project is public.


    type (success, str, NORMAL)
      Bitbucket project type.


    self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO'}])
      Links to Bitbucket project.







Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

