.. _bitbucket_project_module:


bitbucket_project -- Manage your projects on Bitbucket Server
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages Bitbucket Server projects.

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


  project_key (True, str, None)
    Bitbucket project key.


  name (False, str, None)
    Bitbucket project name.

    Required when *state=present*.


  description (False, str, None)
    Bitbucket project description.

    Required when *state=present*.


  avatar (False, str, None)
    Bitbucket project custom avatar. Base64-encoded image data.


  state (False, str, present)
    Whether the project should exist or not.


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

    
    - name: Create project
      esp.bitbucket.bitbucket_project:
        url: 'https://bitbucket.example.com'
        username: admin
        password: secrect
        project_key: FOO
        project_name: A new Bitbucket project
        description: |
            This is a new Bitbucket project.
        validate_certs: no
        state: present

    - name: Create project with custom avatar using token
      esp.bitbucket.bitbucket_project:
        url: 'https://bitbucket.example.com'
        token: 'MjA2M...hqP58'
        project_key: FOO
        name: A new Bitbucket project
        description: |
            This is a new Bitbucket project
        avatar: "{{ lookup('file', 'avatar.png', errors='ignore') | b64encode }}"
        validate_certs: no
        state: present

    - name: Delete project
      esp.bitbucket.bitbucket_project:
        url: 'https://bitbucket.example.com'
        username: admin
        password: secrect
        project_key: FOO
        validate_certs: no
        state: absent



Return Values
-------------

key (success, str, FOO)
  Bitbucket project key.


name (success, str, A new Bitbucket project)
  Bitbucket project name (if *state=present*).


description (success, str, This is a new Bitbucket project)
  Bitbucket project description (if *state=present*).


public (success, bool, False)
  Whether or not the project is public (if *state=present*).


type (success, str, NORMAL)
  Bitbucket project type (if *state=present*).


id (success, int, 200)
  Project ID (if *state=present*).


links (success, dict, )
  Links to Bitbucket project (if *state=present*).


  self (success, list, [{'href': 'https://bitbucket.example.com/projects/FOO'}])
    Links to Bitbucket repository.






Status
------





Authors
~~~~~~~

- Krzysztof Lewandowski (@klewan)
- Evgeniy Krysanov (@catcombo)

