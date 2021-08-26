.. _bitbucket_push_module:


bitbucket_push -- Commit and push changes to the remote repository
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Pushes changes to remote Bitbucket repository.

Optionally, before pushing changes, it creates a new commit containing the current contents of the index and the working tree.

Returns the commit hash.

Authentication can be done with *token* or with *username* and *password*.






Parameters
----------

  commit (optional, bool, True)
    Commit changes before pushing to the remove repository.


  repodir (True, str, None)
    Repository directory.

    This must be a valid git repository.


  msg (True, str, None)
    Log message describing the changes.


  committer (True, dict, None)
    A person who commits the code.


    name (True, str, None)
      The committer username.


    email (True, str, None)
      The committer email address.



  tag (False, str, None)
    Opitionally add a tag to the commit.


  delete (optional, bool, False)
    Delete local repository after push to remote.


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
   - requirements [ os, pathlib, gitpython ]
   - Supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Commit and push changes to the remote repository
      esp.bitbucket.bitbucket_push:
        url: 'https://bitbucket.example.com'
        username: jsmith
        password: secrect
        repository: bar
        project_key: FOO
        path: /tmp/bar  
        commit: yes  
        msg: New commit message
        committer:
          name: jsmith
          email: jsmith@example.com
        tag: '0.3.1'
        delete: no
        validate_certs: no
      register: _result



Return Values
-------------

changed (success, bool, True)
  Whether or not changes were pushed to a remote repository.


json (success, dict, )
  Dictionary with change details.


  author (success, dict, {'email': 'john.smith@example.com', 'name': 'jsmith'})
    Commit request author.


  committer (success, dict, {'email': 'john.smith@example.com', 'name': 'jsmith'})
    Committer.


  msg (success, str, Commit message)
    Commit message.


  before_commit_hexsha (success, str, c1bd91851a8f5b2b147d252ba674329773e7f675)
    A commit hash of the working tree before changes were committed.


  after_commit_hexsha (success, str, 06bdcc6594831af4fe869b87643efc609d7cd994)
    New commit hash. Exposed only when changes were actually committed, i.e. when ``changed=true``.


  tag (success, str, 0.3.1)
    Commit tag.


  deleted (success, bool, False)
    Whether the local repository was deleted after push to remote.






Status
------





Authors
~~~~~~~

- Pawel Smolarz (pawel.smolarz@nordea.com)
- Krzysztof Lewandowski (@klewan)

