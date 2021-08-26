# -*- coding: utf-8 -*-

# Author: Krzysztof Lewandowski <Krzysztof.Lewandowski@nordea.com>,Pawel Smolarz <Pawel.Smolarz@nordea.com>

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import time
import pathlib
import os
import stat
import git

from os import close
from tempfile import mkstemp
from traceback import format_exc

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.urls import fetch_url, basic_auth_header

#
# class: BitbucketHelper
#

class BitbucketHelper:
    BITBUCKET_API_URL = 'https://bitbucket.example.com'

    BITBUCKET_API_ENDPOINTS = {
        'directories-list': '{url}/plugins/servlet/embedded-crowd/directories/list',
        'projects': '{url}/rest/api/1.0/projects',
        'projects-projectKey': '{url}/rest/api/1.0/projects/{projectKey}',
        'projects-permissions': '{url}/rest/api/1.0/projects/{projectKey}/permissions',
        'repos': '{url}/rest/api/1.0/projects/{projectKey}/repos',
        'repos-repositorySlug': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}',
        'repos-permissions': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/permissions',
        'repos-commits': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/commits',
        'repos-browse': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/browse',
        'repos-raw-path': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/raw/{path}{at}',
        'repos-files': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/files',
        'branches': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/branches',
        'branch-permissions-projects': '{url}/rest/branch-permissions/2.0/projects/{projectKey}/restrictions',
        'branch-permissions-repos': '{url}/rest/branch-permissions/2.0/projects/{projectKey}/repos/{repositorySlug}/restrictions',
        'webhooks': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/webhooks',
        'pulls': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests',
        'pulls-delete': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullid}',
        'branch-default': '{url}/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/branches/default',
        'applinks': '{url}/rest/applinks/3.0/applinks',
        'reviewers-project': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/condition',
        'reviewers-get-project': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/conditions',
        'reviewers-project-delete': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/condition/{id}',
        'reviewers-repo': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/repos/{repositorySlug}/condition',
        'reviewers-repo-delete': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/repos/{repositorySlug}/condition/{id}',
        'reviewers-get-repo': '{url}/rest/default-reviewers/1.0/projects/{projectKey}/repos/{repositorySlug}/conditions',
        'user': '{url}/rest/api/1.0/users/{userId}',
    }

    def __init__(self, module):
        self.module = module
        self.module.params['url_username'] = self.module.params['username']
        self.module.params['url_password'] = self.module.params['password']
        if self.module.params['url'] is None:
            self.module.params['url'] = self.BITBUCKET_API_URL

    @staticmethod
    def bitbucket_argument_spec():
        return dict(
            url=dict(type='str', no_log=False, required=False),
            username=dict(type='str', no_log=False, required=False, default=None, aliases=['user'],
                          fallback=(env_fallback, ['BITBUCKET_USER_ID'])),
            password=dict(type='str', no_log=True, required=False, default=None),
            token=dict(type='str', no_log=True, required=False, default=None,
                       fallback=(env_fallback, ['BITBUCKET_ACCESS_TOKEN'])),
            validate_certs=dict(type='bool', default=True),
            use_proxy=dict(type='bool', default=True),
            force_basic_auth=dict(type='bool', default=True),
            return_content=dict(type='bool', default=True),
            sleep=dict(type='int', default=5),
            retries=dict(type='int', default=3),
        )

    def request(self, api_url, method, data=None, headers=None):
        headers = headers or {}

        if self.module.params['token']:
            headers.update({
                'Authorization': 'Bearer {0}'.format(self.module.params['token']),
            })
            self.module.params['force_basic_auth'] = False
        # else:
        #    headers.update({
        #        'Authorization': basic_auth_header(self.module.params['username'], self.module.params['password'])
        #    })

        if isinstance(data, dict):
            data = self.module.jsonify(data)
            # headers.update({
            #     'Content-type': 'application/json',
            # })
            if not ('Content-type' in headers):
                headers.update({
                    'Content-type': 'application/json',
                })

        retries = 1
        while retries <= self.module.params['retries']:
            response, info = fetch_url(
                module=self.module,
                url=api_url,
                method=method,
                headers=headers,
                data=data,
                force=True,
                use_proxy=self.module.params['use_proxy'],
            )
            if (info is not None) and (info['status'] != -1):
                break
            time.sleep(self.module.params['sleep'])
            retries += 1

        content = {}
   
        if response is not None:

            body = to_text(response.read())
            if body:
                try:
                    js = json.loads(body)
                    if isinstance(js, dict):
                        content = js
                    else:
                        content['json'] = js
                except ValueError as e:
                    content['content'] = body

        content['fetch_url_retries'] = retries

        return info, content

    def listify_comma_sep_strings_in_list(self, some_list):
        """
        method to accept a list of strings as the parameter, find any strings
        in that list that are comma separated, remove them from the list and add
        their comma separated elements to the original list
        """
        new_list = []
        remove_from_original_list = []
        for element in some_list:
            if ',' in element:
                remove_from_original_list.append(element)
                new_list.extend([e.strip() for e in element.split(',')])

        for element in remove_from_original_list:
            some_list.remove(element)

        some_list.extend(new_list)

        if some_list == [""]:
            return []

        return some_list

    def get_project_info(self, fail_when_not_exists=False, project_key=None):
        """
        Search for an existing project on Bitbucket

        when fail_when_not_exists=False it just returns None and does not fail
        """
        info, content = self.request(
            api_url=self.BITBUCKET_API_ENDPOINTS['projects-projectKey'].format(
                url=self.module.params['url'],
                projectKey=project_key,
            ),
            method='GET',
        )

        if info['status'] == 200:
            return content

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to view `{projectKey}` project.'.format(
                    projectKey=project_key,
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{projectKey}` project does not exist.'.format(
                    projectKey=project_key,
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve the project data which matches the supplied projectKey `{projectKey}`: {info}'.format(
                    projectKey=project_key,
                    info=info,
                ))

        return None

    def get_all_projects_info(self, fail_when_not_exists=False):
        """
        Search for all existing projects on Bitbucket for which the authenticated user has the PROJECT_VIEW permission.

        """
        projects = []

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS['projects'] + '?limit=1000&start={nextPageStart}').format(
                    url=self.module.params['url'],
                    nextPageStart=nextPageStart,
                ),
                method='GET',
            )

            projects.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return projects

        if info['status'] == 400:
            self.module.fail_json(msg='The permission level is unknown or not related to projects')

        if info['status'] != 200:
            self.module.fail_json(msg='Failed to retrieve the projects data.')

        return None

    def get_repository_info(self, fail_when_not_exists=False, project_key=None, repository=None):
        """
        Search for an existing repository on Bitbucket

        when fail_when_not_exists=False it just returns None and does not fail
        """
        info, content = self.request(
            api_url=self.BITBUCKET_API_ENDPOINTS['repos-repositorySlug'].format(
                url=self.module.params['url'],
                projectKey=project_key,
                repositorySlug=repository,
            ),
            method='GET',
        )

        if info['status'] == 200:
            return content

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to see `{repositorySlug}` repository.'.format(
                    repositorySlug=repository,
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{repositorySlug}` repository does not exist.'.format(
                    repositorySlug=repository,
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve the repository data which matches the supplied projectKey `{projectKey}` and repositorySlug `{repositorySlug}`: {info}'.format(
                    projectKey=project_key,
                    repositorySlug=repository,
                    info=info,
                ))

        return None

    def get_all_repositories_info(self, fail_when_not_exists=False):
        """
        Search for all existing repositories for the supplied project for which the authenticated user has the REPO_READ permission.

        """
        repositories = []

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS['repos'] + '?limit=1000&start={nextPageStart}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    nextPageStart=nextPageStart,
                ),
                method='GET',
            )

            repositories.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return repositories

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to see `{projectKey}` project.'.format(
                    projectKey=self.module.params['project_key'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{projectKey}` project does not exist.'.format(
                    projectKey=self.module.params['project_key'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(msg='Failed to retrieve the repository data.')

        return None

    def get_branches_info(self, fail_when_not_exists=False, filter=None):
        """
        Retrieve the branches matching the supplied filter

        when fail_when_not_exists=False it just returns None and does not fail
        """
        branches = []

        filterText = ""
        if filter is not None:
            filterText = "&filterText=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'branches'] + '?limit=1000&start={nextPageStart}&details=false{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            branches.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return branches

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to read `{repositorySlug}` repository.'.format(
                    repositorySlug=self.module.params['repository'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{repositorySlug}` repository does not exist.'.format(
                    repositorySlug=self.module.params['repository'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve branches data which matches the supplied projectKey `{projectKey}` and repositorySlug `{repositorySlug}`: {info}'.format(
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    info=info,
                ))

        return None

    def get_project_permissions_info(self, fail_when_not_exists=False, project_key=None, scope=None, filter=None):
        """
        Retrieve users or groups that have been granted at least one permission for the specified project.
        scope: either 'users' or 'groups'.

        when fail_when_not_exists=False it just returns None and does not fail
        """
        permissions = []

        filterText = ""
        if filter is not None:
            filterText = "&filter=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'projects-permissions'] + '/{scope}?limit=1000&start={nextPageStart}{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=project_key,
                    scope=scope,
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            permissions.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return permissions

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user is not a project administrator for {projectKey} project.'.format(
                    projectKey=project_key,
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='Project `{projectKey}` does not exist.'.format(
                    projectKey=project_key,
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve permission data which matches the supplied projectKey `{projectKey}`: {info}'.format(
                    projectKey=project_key,
                    info=info,
                ))

        return None

    def get_repository_permissions_info(self, fail_when_not_exists=False, project_key=None, repository=None, scope=None,
                                        filter=None):
        """
        Retrieve users or groups that have been granted at least one permission for the specified repository.
        scope: either 'users' or 'groups'.

        when fail_when_not_exists=False it just returns None and does not fail
        """
        permissions = []

        filterText = ""
        if filter is not None:
            filterText = "&filter=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'repos-permissions'] + '/{scope}?limit=1000&start={nextPageStart}{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=project_key,
                    repositorySlug=repository,
                    scope=scope,
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            permissions.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return permissions

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user is not a repository administrator for {projectKey} project and {repositorySlug} repository.'.format(
                    projectKey=project_key,
                    repositorySlug=repository,
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='Repository `{repositorySlug}` does not exist.'.format(
                    repositorySlug=repository,
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve permission data which matches the supplied repository `{repositorySlug}`: {info}'.format(
                    repositorySlug=repository,
                    info=info,
                ))

        return None


    def get_branch_permissions_info(self, fail_when_not_exists=False, project_key=None, repository=None):
        """
        Search for branch restrictions for the supplied project or repository.

        when fail_when_not_exists=False it just returns None and does not fail
        """
        restrictions = []

        isLastPage = False
        nextPageStart = 0

        if repository is None:
            url = (self.BITBUCKET_API_ENDPOINTS[
                                'branch-permissions-projects'] + '/?limit=1000&start={nextPageStart}').format(
                        url=self.module.params['url'],
                        projectKey=project_key,
                        nextPageStart=nextPageStart,
            )
        else:
            url = (self.BITBUCKET_API_ENDPOINTS[
                                'branch-permissions-repos'] + '/?limit=1000&start={nextPageStart}').format(
                        url=self.module.params['url'],
                        projectKey=project_key,
                        repositorySlug=repository,
                        nextPageStart=nextPageStart,
            )
        
        while not isLastPage:
            info, content = self.request(
                api_url=url,
                method='GET',
            )

            restrictions.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] == 200:
            return restrictions

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='The restriction could not be found')
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve restriction which matches the supplied project and/or repository: {info}'.format(
                    info=info,
                ))

        return None


    def get_webhooks_info(self, fail_when_not_exists=False, filter=None):
        """
        Retrieve the webhooks matching the supplied filter

        when fail_when_not_exists=False it just returns None and does not fail
        """
        webhooks = []

        filterText = ""
        if filter is not None:
            filterText = "&filterText=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'webhooks'] + '?limit=1000&start={nextPageStart}&details=false{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            webhooks.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] in [200,201]:
            return webhooks

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to read `{repositorySlug}` repository.'.format(
                    repositorySlug=self.module.params['repository'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{repositorySlug}` repository does not exist.'.format(
                    repositorySlug=self.module.params['repository'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve branches data which matches the supplied projectKey `{projectKey}` and repositorySlug `{repositorySlug}`: {info}'.format(
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    info=info,
                ))

        return None


    def get_pull_request_info(self, fail_when_not_exists=False, filter=None):
        """
        Retrieve the pulls matching the supplied filter

        when fail_when_not_exists=False it just returns None and does not fail
        """
        pulls = []

        filterText = ""
        if filter is not None:
            filterText = "&filterText=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'pulls'] + '?limit=1000&start={nextPageStart}&details=false{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            pulls.extend(content['values'])

            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] in [200,201]:
            return pulls

        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to read `{repositorySlug}` repository.'.format(
                    repositorySlug=self.module.params['repository'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{repositorySlug}` repository does not exist.'.format(
                    repositorySlug=self.module.params['repository'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve branches data which matches the supplied projectKey `{projectKey}` and repositorySlug `{repositorySlug}`: {info}'.format(
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    info=info,
                ))

        return None

    def get_project_reviewers(self, fail_when_not_exists=False, filter=None):
        """
        Retrieve the project reviewers matching the supplied filter

        when fail_when_not_exists=False it just returns None and does not fail
        """
        reviewers = []

        filterText = ""
        if filter is not None:
            filterText = "&filterText=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'reviewers-get-project'] + '?limit=1000&start={nextPageStart}&details=false{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            reviewers.extend(content['json'])
            # reviewers.extend(content['values'])
            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] in [200,201]:
            return reviewers
            # self.module.fail_json(
            #     msg='Check info: `{info}`, reviewers: `{reviewers}`'.format(
            #         info=info,
            #         reviewers=reviewers,
            #     ))
        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to read `{projectKey}` project settings.'.format(
                    projectKey=self.module.params['project_key'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{projectKey}` project does not exist.'.format(
                    projectKey=self.module.params['project_key'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve default project reviewers data which matches the supplied projectKey `{projectKey}`: {info}'.format(
                    projectKey=self.module.params['project_key'],
                    info=info,
                ))

        return None

    def get_repo_reviewers(self, fail_when_not_exists=False, filter=None):
        """
        Retrieve the repository reviewers matching the supplied filter

        when fail_when_not_exists=False it just returns None and does not fail
        """
        reviewers = []

        filterText = ""
        if filter is not None:
            filterText = "&filterText=%s" % filter

        isLastPage = False
        nextPageStart = 0

        while not isLastPage:
            info, content = self.request(
                api_url=(self.BITBUCKET_API_ENDPOINTS[
                             'reviewers-get-repo'] + '?limit=1000&start={nextPageStart}&details=false{filterText}').format(
                    url=self.module.params['url'],
                    projectKey=self.module.params['project_key'],
                    repositorySlug=self.module.params['repository'],
                    nextPageStart=nextPageStart,
                    filterText=filterText,
                ),
                method='GET',
            )

            reviewers.extend(content['json'])
            if 'isLastPage' in content:
                isLastPage = content['isLastPage']
                if 'nextPageStart' in content:
                    nextPageStart = content['nextPageStart']
            else:
                isLastPage = True

        if info['status'] in [200,201]:
            return reviewers
            # self.module.fail_json(
            #     msg='Check reviewers: `{reviewers}`.'.format(
            #         reviewers=reviewers
            #     ))
        if info['status'] == 401:
            self.module.fail_json(
                msg='The currently authenticated user has insufficient permissions to read `{repositorySlug}` repository settings.'.format(
                    repositorySlug=self.module.params['repository'],
                ))

        if info['status'] == 404:
            if fail_when_not_exists:
                self.module.fail_json(msg='`{repositorySlug}` project does not exist.'.format(
                    repositorySlug=self.module.params['repository'],
                ))
            else:
                return None

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve default repostory reviewers data which matches the supplied repository ID `{repositorySlug}`: {info}'.format(
                    repositorySlug=self.module.params['repository'],
                    info=info,
                ))

        return None

    def get_application_links_info(self):
        """
        Search for an existing Application Links on Bitbucket

        """
        info, content = self.request(
            api_url=self.BITBUCKET_API_ENDPOINTS['applinks'].format(
                url=self.module.params['url'],
                headers = {
                    'Content-type': 'application/json',
                },
            ),
            method='GET',
        )

        if info['status'] == 200:
            return content

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve the application links data`: {info}'.format(
                    info=info,
                ))

        return None

    def get_users_id(self, userid=None):
        """
        Search for information about user

        """
        info, content = self.request(
            api_url=self.BITBUCKET_API_ENDPOINTS['user'].format(
                url=self.module.params['url'],
                userId=userid,
                headers = {
                    'Content-type': 'application/json',
                },
            ),
            method='GET',
        )

        if info['status'] == 200:
            return content['id']

        if info['status'] != 200:
            self.module.fail_json(
                msg='Failed to retrieve the user information. Please be sure that user exists`: {info}'.format(
                    info=info,
                ))

        return None

    def create_git_askpass_script(self):
        """
        Create a temporary script to inject git credentials for use with git remote repository commands, i.e. clone, fetch, pull and push.
        It is intended to be called by Git via GIT_ASKPASS.
        Requires GIT_USERNAME and GIT_PASSWORD environment variables.
        GIT_PASSWORD can be a token.

        :return:
            path to the git_askpass script
        """
        try:
            handle, path = mkstemp(prefix='ansible.', text=True)
            close(handle)
            os.chmod(path, stat.S_IRWXU)

        except Exception as e:
            self.module.fail_json(msg=to_native(e), exception=format_exc())

        content = """
#!/bin/sh
case "$1" in
Username*) echo $GIT_USERNAME ;;
Password*) echo $GIT_PASSWORD ;;
esac
""".strip()

        with open(path, 'w') as f:
            f.write(content)

        return path


    @staticmethod
    def bb_dest_exists(destination_dir, module, msg):
        """ Return formated destination directory
            Create directory if not exists
        """
        repo_dest = pathlib.Path(destination_dir)

        if repo_dest.exists() and repo_dest.is_dir():
            msg.append('Parent directory %s for repository exists' % (destination_dir))
        else:
            try:
                os.makedirs(destination_dir)
            except OSError:
                msg.append('Creation of parent directory %s for repository failed' % (destination_dir))
                module.fail_json(msg=msg, changed=False)
            else:
                msg.append('Successfully created the parent directory %s for repository' % (destination_dir))
        if destination_dir[-1] == '/':
            return destination_dir
        else:
            return destination_dir + '/'


    @staticmethod
    def bb_check_repo_dir(repo_path, module, msg, ):
        """ Return a boolean
            False if repository directory not exists,
            failed if directory exists but is not git repo
        """
        repo_dir = pathlib.Path(repo_path)
        if repo_dir.exists():
            try:
                _ = git.Repo(repo_path).git_dir
                msg.append('Repository %s is correct git repository' % (repo_path))
                return True
            except git.exc.InvalidGitRepositoryError:
                msg.append('Directory exists %s is not correct git repository' % (repo_path))
                module.fail_json(msg=msg, changed=False)
        else:
            return False


    def set_default_branch(self, branch=None):
        """
        Update the default branch of a repository.

        """        
        info, content = self.request(
            api_url=self.BITBUCKET_API_ENDPOINTS['branch-default'].format(
                url=self.module.params['url'],
                projectKey=self.module.params['project_key'],
                repositorySlug=self.module.params['repository'],
            ),
            method='PUT',
            data={
                'id': "refs/heads/" + branch
            },
        )

        if info['status'] == 204:
            return content

        if info['status'] == 401:
            module.fail_json(
                msg='The currently authenticated user has insufficient permissions to update `{repositorySlug}` repository'.format(
                    repositorySlug=self.module.params['repository'],
                ))

        if info['status'] == 404:
            module.fail_json(msg='Repository `{repositorySlug}` does not exist.'.format(
                repositorySlug=self.module.params['repository'],
            ))

        if info['status'] != 204:
            module.fail_json(
                msg='Failed to set default branch to `{branch}` for the supplied `{repositorySlug}` repository and `{projectKey}` project: {info}'.format(
                    branch=branch,
                    repositorySlug=self.module.params['repository'],
                    projectKey=self.module.params['project_key'],
                    info=info,
                ))

        return None