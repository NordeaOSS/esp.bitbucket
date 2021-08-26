# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<br>

### [1.4.1] - 2021-08-26

Updated documentation

### [1.4.0] - 2021-08-03
Added the following modules:
- [bitbucket_project_reviewer](plugins/modules/bitbucket_project_reviewer.py) 
- [bitbucket_repo_reviewer](plugins/modules/bitbucket_repo_reviewer.py)

### [1.3.1] - 2021-07-28

#### Changed:

- Fix [git_commit](plugins/modules/git_commit.py)
    - Error: `TypeError: send() got multiple values for keyword argument 'MESSAGE'` fixed by changing module parameter from message to msg
    - Alias message added
- Fix [bitbucket_push](plugins/modules/bitbucket_push.py)
    - Error: `TypeError: send() got multiple values for keyword argument 'MESSAGE'` fixed by changing module parameter from message to msg
    - Alias message added

### [1.3.0] - 2021-06-04

#### Changed:

- Renamed `bitbucket_commit` to [git_commit](plugins/modules/git_commit.py)
    - Added new options to [git_commit](plugins/modules/git_commit.py), i.e. `committer` and `tag`. 
    - [git_commit](plugins/modules/git_commit.py) returns commit hash, i.e. `before_commit_hexsha` and `after_commit_hexsha`.
    - Added `check_mode` support.

- Renamed `bitbucket_init` to [git_init](plugins/modules/git_init.py)
    - Added `check_mode` support.

- Redesigned [bitbucket_push](plugins/modules/bitbucket_push.py) module
    - Added `commit` option to commit all pending changes before pushing changes to Bitbucket.
    - [bitbucket_push](plugins/modules/bitbucket_push.py) now commits changes and pushes the to Bitbucket.
    - Module uses `GIT_ASKPASS` functionality for authentication.
    - Returns commit hash, i.e. `before_commit_hexsha` and `after_commit_hexsha`.
    - Added `check_mode` support.

- Redesigned [bitbucket_clone](plugins/modules/bitbucket_clone.py) module
    - Module uses `GIT_ASKPASS` functionality for authentication.
    - Returns the latest commit hash of the cloned repository branch, i.e. `commit_hexsha`.
    - Added `check_mode` support.


<br>

### [1.2.5] - 2021-05-19

#### Fixed:

- [bitbucket_clone](plugins/modules/bitbucket_clone.py) - token alias added, username and password required together
- [bitbucket_push](plugins/modules/bitbucket_push.py) - token alias added, username and password required together

<br>

### [1.2.4] - 2021-05-05

#### Fixed:

- [bitbucket_slurp](plugins/modules/bitbucket_slurp.py) - fixed Python 3 dependency

<br>

### [1.2.3] - 2021-04-28

#### Changed:

- [bitbucket_push](samples/bitbucket_push/sample.yml) - `dest` added to example playbook
- [bitbucket_clone](samples/bitbucket_clone/sample.yml) - `dest` added to example playbook

<br>

### [1.2.2] - 2021-04-28

#### Changed:

- [bitbucket_clone](plugins/modules/bitbucket_clone.py) - added `force` option
- [bitbucket_push](plugins/modules/bitbucket_push.py) - added `delete` option

<br>

### [1.2.1] - 2021-04-27

#### Fixed:

- [bitbucket_copy](plugins/modules/bitbucket_copy.py) - md5 calculation

<br>

### [1.2.0] - 2021-04-22

#### Added:

New release of collection modules.

- Added the following modules:
    - [bitbucket_application_link](plugins/modules/bitbucket_application_link.py)
    - [bitbucket_application_link_info](plugins/modules/bitbucket_application_link_info.py)    
    
#### Fixed:

#### Changed:

#### Deprecated:

<br>

### [1.1.0] - 2021-04-16

#### Added:

New release of collection modules.

- Added the following modules:
    - [bitbucket_branch_permissions](plugins/modules/bitbucket_branch_permissions.py)
    - [bitbucket_default_branch](plugins/modules/bitbucket_default_branch.py)    
    - [bitbucket_pull_request](plugins/modules/bitbucket_pull_request.py)
    - [bitbucket_pull_request_info](plugins/modules/bitbucket_pull_request_info.py)
    - [bitbucket_find](plugins/modules/bitbucket_find.py)
    - [bitbucket_copy](plugins/modules/bitbucket_copy.py)    

- Added the following lookups:
    - [bitbucket_fileglob](plugins/lookup/bitbucket_fileglob.py)

#### Fixed:

#### Changed:

- Added `is_default` parameter to [bitbucket_branch](plugins/modules/bitbucket_branch.py)

#### Deprecated:

<br>

### [1.0.0] - 2021-04-12

#### Added:

New release of collection modules.

- Added the following modules:
    - [bitbucket_project](plugins/modules/bitbucket_project.py)
    - [bitbucket_project_info](plugins/modules/bitbucket_project_info.py)
    - [bitbucket_project_permissions](plugins/modules/bitbucket_project_permissions.py)
    - [bitbucket_project_permissions_info](plugins/modules/bitbucket_project_permissions_info.py)
    - [bitbucket_repo](plugins/modules/bitbucket_repo.py)
    - [bitbucket_repo_info](plugins/modules/bitbucket_repo_info.py)
    - [bitbucket_repo_permissions](plugins/modules/bitbucket_repo_permissions.py)
    - [bitbucket_repo_permissions_info](plugins/modules/bitbucket_repo_permissions_info.py)
    - [bitbucket_slurp](plugins/modules/bitbucket_slurp.py)
    - [bitbucket_clone](plugins/modules/bitbucket_clone.py)
    - [bitbucket_commit](plugins/modules/bitbucket_commit.py)
    - [bitbucket_init](plugins/modules/bitbucket_init.py)
    - [bitbucket_push](plugins/modules/bitbucket_push.py)
    - [bitbucket_directory_sync](plugins/modules/bitbucket_directory_sync.py)
    - [bitbucket_branch](plugins/modules/bitbucket_branch.py)
    - [bitbucket_branch_info](plugins/modules/bitbucket_branch_info.py)
    - [bitbucket_branch_permissions_info](plugins/modules/bitbucket_branch_permissions_info.py)
    - [bitbucket_webhook](plugins/modules/bitbucket_webhook.py)
    - [bitbucket_webhook_info](plugins/modules/bitbucket_webhook_info.py)

- Added the following lookups:
    - [bitbucket_file](plugins/lookup/bitbucket_file.py)
    
- Support for access token authentication

#### Fixed:

#### Changed:

#### Deprecated:
