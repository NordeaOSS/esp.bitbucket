.. _bitbucket_project_reviewer_module:


bitbucket_project_reviewer -- Manage default reviewer setting on project level
==============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Configure default reviewers for project

Only projects for which the authenticated user has the admin right can be managed.

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


  project_key (True, list, None)
    Retrieve projects matching the supplied *project_key* filter.

    This can be '*' which means all projects.


  validate_certs (optional, bool, True)
    If ``no``, SSL certificates will not be validated.

    This should only set to ``no`` used on personally controlled sites using self-signed certificates.


  use_proxy (optional, bool, True)
    If ``no``, it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  sleep (optional, int, 5)
    Number of seconds to sleep between API retries.


  retries (optional, int, 3)
    Number of retries to call Bitbucket API URL before failure.


  reviewers (True, list, None)
    List of project default reviewers


  branch (True, str, master)
    Branch name


  approvals (False, str, 0)
    Number of approvals required





Notes
-----

.. note::
   - Bitbucket Access Token can be obtained from Bitbucket profile -> Manage Account -> Personal Access Tokens.
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Configure default reviewer globally on AIMT project for master branch
      esp.bitbucket.bitbucket_project_reviewer:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        project_key: 'AIMT'
        validate_certs: no
        reviewers: [ user1 ]
        branch: 'master'



Return Values
-------------

messages (always, list, ['Repository `bar2` does not exist.'])
  List of error messages.


projects (always, list, )
  List of Bitbucket projects.


  key (success, str, FOO)
    Bitbucket project key.


  name (success, str, A new Bitbucket project)
    Bitbucket project name.


  description (success, str, This is a new Bitbucket project)
    Bitbucket project description.


  public (success, bool, False)
    Whether or not the project is public.


  type (success, str, NORMAL)
    Bitbucket project type.


  id (success, int, 200)
    Project ID.


  links (success, dict, )
    Links to Bitbucket project.


    self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO'}])
      Links to Bitbucket repository.







Status
------





Authors
~~~~~~~

- Pawel Smolarz (pawel.smolarz@nordea.com)

