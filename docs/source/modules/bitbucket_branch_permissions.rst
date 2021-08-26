.. _bitbucket_branch_permissions_module:


bitbucket_branch_permissions -- Manage restrictions for repository branches.
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create a restriction for the supplied branch to be applied on the given repository or all repositories in the given project.

A restriction means preventing writes on the specified branch by all except a set of users and/or groups, or preventing specific operations such as branch deletion.

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


  repository (False, str, None)
    Repository name.


  project_key (True, str, None)
    Bitbucket project key.


  branch_name (False, str, None)
    A specific branch name you want to restrict access to.

    This is only needed when not using *branch_pattern* and *branching_model*.

    One of *branch_name*, *branch_pattern* and *branching_model* is required.


  branch_pattern (False, str, None)
    A wildcard pattern that may match multiple branches you want to restrict access to.

    This is only needed when not using *branch_name* and *branching_model*.

    One of *branch_name*, *branch_pattern* and *branching_model* is required.


  branching_model (False, str, None)
    Branch prefixes in the Branching model. Select the branch type you want to restrict access to.

    This is only needed when not using *branch_name* and *branch_pattern*.

    One of *branch_name*, *branch_pattern* and *branching_model* is required.


  restrictions (optional, list, None)
    Definition of the restrictions for repository branches.


    prevent (True, str, None)
      Restriction name.


    exemptions (optional, dict, None)
      Exemptions from the supplied restriction.


      groups (optional, list, None)
        Groups excluded from the restriction.


      users (optional, list, None)
        Users excluded from the restriction.


      access_keys (optional, list, None)
        Access keys excluded from the restriction.




  state (True, str, present)
    Whether the restriction should exist or not.


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

    
    - name: Create restrictions for the supplied branch
      esp.bitbucket.bitbucket_branch_permissions:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        branch_name: master
        restrictions:
          - prevent: deletion
          - prevent: rewriting history
            exemptions:
              groups: [ group1, group2 ]
              users: [ amy ]
              access_keys: []
          - prevent: changes without a pull request
            exemptions:
              groups: [ group3 ]
              users: [ joe ]
              access_keys: []                    
        state: present
        validate_certs: no

    - name: Create restrictions for the supplied branches - bugfix branches - on all repositories in the given project
      esp.bitbucket.bitbucket_branch_permissions:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: FOO
        branching_model: bugfix
        restrictions:
          - prevent: all changes
            exemptions:
              groups: [ group1, group2 ]
              users: [ amy ]
              access_keys: []
        state: present
        validate_certs: no

    - name: Create restrictions for the supplied branches - matching branch_pattern - on the given repository
      esp.bitbucket.bitbucket_branch_permissions:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        branch_pattern: develop
        restrictions:
          - prevent: deletion
          - prevent: changes without a pull request
            exemptions:
              groups: [ group4 ]
              users: [ john ]
        state: present
        validate_certs: no

    - name: Delete restrictions for the supplied branch
      esp.bitbucket.bitbucket_branch_permissions:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: FOO    
        repository: bar  
        branch_name: master
        restrictions:
          - prevent: 'deletion'
            exemptions:
              groups: []
              users: [ john ]
              access_keys: []        
          - prevent: 'rewriting history'
        state: absent
        validate_certs: no



Return Values
-------------

project_key (always, str, FOO)
  Bitbucket project key.


repository (always, str, bar)
  Bitbucket repository name.


branch_name (success, str, master)
  A specific branch name.


branch_pattern (success, str, develop)
  A wildcard pattern that may match multiple branches.


branching_model (success, str, bugfix)
  Branch prefixes in the Branching model.


results (success, list, )
  List of affected branch permissions.


  matcher (success, dict, {'active': True, 'displayId': 'Release', 'id': 'RELEASE', 'type': {'id': 'MODEL_CATEGORY', 'name': 'Branching model category'}})
    Matcher description.


  scope (success, dict, {'resourceId': 292, 'type': 'PROJECT'})
    Scope.


  id (success, int, 42)
    Permission ID.


  groups (success, list, ['bitbucket-admin'])
    Bitbucket groups.


  users (success, list, ['joe', 'jsmith'])
    Bitbucket users.


  accessKeys (success, list, [])
    Bitbucket access keys.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)

