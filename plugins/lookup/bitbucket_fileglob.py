# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
name: bitbucket_fileglob
author: Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
version_added: 1.1.0
short_description: Retrieve a list of files from particular repository of a Bitbucket Server
description:
  - Retrieve a list of matching file names from particular repository of a Bitbucket Server. 
  - Files are selected based on C(_terms) option. Additionaly, files can be further filtered out by C(grep) option to select only those matching the supplied grep pattern.
  - Combined outcome of C(_terms) and C(grep) options form the final list of files returned by this lookup.
  - The search is done using Python regex patterns.
options:
  _terms:
    description: List of Python regex patterns to search for in file names on a Bitbucket Server repository.
    required: True
  url:
    description:
    - Bitbucket Server URL.
    type: str
    required: false
  at:
    description:
    - The commit ID or ref (e.g. a branch or tag) to read a file at.
    - If not specified the default branch will be used instead.
    type: str
    required: false
  username:
    description:
    - Username used for authentication.
    - This is only needed when not using I(token).
    - Required when I(password) is provided.
    type: str
    required: false
  password:
    description:
    - Password used for authentication.
    - This is only needed when not using I(token).
    - Required when I(username) is provided.
    type: str
    required: false
  token:
    description:
    - Token parameter for authentication.
    - This is only needed when not using I(username) and I(password).
    type: str
    required: false
  repository:
    description:
    - Repository name.
    type: str
    required: true
  project_key:
    description:
    - Bitbucket project key.
    type: str
    required: true
  grep:
    description:
    - Python regex pattern to search for in each file selected from repository to form the final list of files.
    - Files are selected based on C(_terms) option.
    - Combined outcome of C(_terms) and C(grep) options form the final list of files returned by this module.
    - If not specified, search will not be executed.
    type: str  
    required: false    
  validate_certs:
    description:
    - If C(no), SSL certificates will not be validated.
    - This should only set to C(no) used on personally controlled sites using self-signed certificates.
    type: bool
    default: yes
    required: false
  use_proxy:
    description:
    - If C(no), it will not use a proxy, even if one is defined in an environment variable on the target hosts.
    type: bool
    default: no 
    required: false
  sleep:
    description:
    - Number of seconds to sleep between API retries.
    type: int
    default: 5
    required: false
  retries:
    description:
    - Number of retries to call Bitbucket API URL before failure.
    type: int
    default: 3
    required: false
notes:
  - Returns a string list of paths joined by commas, or an empty list if no files match. For a 'true list' pass C(wantlist=True) to the lookup.
'''

EXAMPLES = """
- name: Display paths of all files in a repository - returns a true list
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_fileglob', '.+',
             project_key='FOO', repository='bar', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret', wantlist=True) }}"  

- name: Display paths of all files from a repository that end specific way - returns a string list of paths joined by commas
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_fileglob', '.+\\.yml$', '.+\\.json$', '.+\\.txt$',
             project_key='FOO', repository='bar', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret') }}"  

- name: Display paths of all files with 'baz' in their names in develop branch and with the supplied grep pattern in the files content - returns a true list
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_fileglob', 'baz', grep='hello.+world',
             project_key='FOO', repository='bar', at='develop', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret', wantlist=True) }}"  

- name: Add a line to a report file for each file found in the specified directories on Bitbucket repository
  ansible.builtin.lineinfile:
    path: /tmp/report.txt
    line: '{{ item }} file found in Bitbucket Server repository'
    create: yes
  loop: "{{ query('esp.bitbucket.bitbucket_fileglob', '^/path/to/dir1/', '^/path/to/dir2/',
            project_key='FOO', repository='bar', at='master', validate_certs='no', 
            url='https://bitbucket.example.com', token='MjA2M...hqP58' ) }}"
  loop_control:
    label: "[Processing {{ item }} file from Bitbucket Server ..]"
"""

RETURN = """
  _raw:
    description:
      - list of files
    type: list
    elements: str
"""

import json
import urllib
import time
import re

import requests
from requests.auth import HTTPBasicAuth

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.urls import basic_auth_header
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)

        all_files = []
        # Retrieve a list of all files of a repository at the specified ref (at). 
        try:
            at = ""
            if self.get_option('at') is not None:
                at = "&at=%s" % self.get_option('at')

            if self.get_option('url') is None:
                api_url = BitbucketHelper.BITBUCKET_API_URL
            else:
              api_url = self.get_option('url')

            isLastPage = False
            nextPageStart = 0

            while not isLastPage:

                url = (BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-files'] + '?limit=1000&start={nextPageStart}{path}{at}').format(
                    url=api_url,
                    projectKey=self.get_option('project_key'),
                    repositorySlug=self.get_option('repository'),
                    nextPageStart=nextPageStart,
                    path='',
                    at=at,
                )

                info, content = self.request(
                    url=url, 
                    method='GET',
                )

                if info['status'] == 200:
                    all_files.extend(content['values'])

                if info['status'] == 400:
                    raise AnsibleError("The path requested is not a directory at the supplied commit.")

                if info['status'] == 404:
                    raise AnsibleError("The specified repository does not exist.")

                if info['status'] != 200:
                    raise AnsibleError("Failed to retrieve a list of files Bitbucket Server.  : {info}".format(
                            info=info,
                        ))

                if 'isLastPage' in content:
                    isLastPage = content['isLastPage']
                    if 'nextPageStart' in content:
                        nextPageStart = content['nextPageStart']
                else:
                    isLastPage = True

        except Exception as e:
            raise AnsibleError("Failed to retrieve a list of files Bitbucket Server. Error was: %s" % (to_native(e)))

        ret = []

        # Compile 'grep' pattern, i.e. PATTERN that is searched in each file selected from repository to form the final list of files
        if self.get_option('grep') is not None:
            try:
                grep = re.compile(self.get_option('grep'))
            except Exception as e:
                raise AnsibleError('Unable to use "%s" as a search parameter: %s' % (self.get_option('grep'), to_native(e)))

        # Itereate over all file patterns
        for term in terms:

            if not isinstance(term, string_types):
                raise AnsibleError('Invalid setting identifier, "%s" is not a string, it is a %s' % (term, type(term)))

            try:
                pattern = re.compile(term)
            except Exception as e:
                raise AnsibleError('Unable to use "%s" as a search parameter: %s' % (term, to_native(e)))

            for file_path in all_files:
                # when file name matches the given pattern
                if pattern.search(file_path):
                    # when 'grep' pattern is defined, read the file content
                    if self.get_option('grep') is not None:
                        file_content = self.slurp_file(project_key=self.get_option('project_key'), repository=self.get_option('repository'), path=file_path)
                        # when file content matches the given pattern (grep), add the file path to the result list
                        if grep.search(file_content):
                            ret.append(file_path)
                    else:                        
                        ret.append(file_path)

        # Make the list of files unique
        return list(set(ret))


    def slurp_file(self, project_key=None, repository=None, path=None):
        """
        Read file content on Bitbucket Server

        """
        at = ""
        if self.get_option('at') is not None:
            at = "?at=%s" % self.get_option('at')

        if self.get_option('url') is None:
            api_url = BitbucketHelper.BITBUCKET_API_URL
        else:
            api_url = self.get_option('url')

        info, content = self.request(
            url=BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-raw-path'].format(
                url=api_url,
                projectKey=project_key,
                repositorySlug=repository,
                path=path,
                at=at,
            ),
            method='GET',
        )

        if info['status'] == 200:
            return content['content']

        if info['status'] != 200:
            raise AnsibleError('Failed to retrieve content of a file which matches the supplied projectKey `{projectKey}`, repositorySlug `{repositorySlug}` and file path `{path}`: {info}'.format(
                projectKey=project_key,
                repositorySlug=repository,
                path=path,
                info=info,
            ))

        return None


    def request(self, url=None, method=None):
        """
        Execute URL request

        """
        headers = {}

        force_basic_auth = True
        if self.get_option('token') is not None:
            headers.update({
                'Authorization': 'Bearer {0}'.format(self.get_option('token')),
            })
            force_basic_auth = False

        iretries = 1
        while iretries <= self.get_option('retries'):
            response, error, info = self.fetch_url(
                                    url=url, 
                                    validate_certs=self.get_option('validate_certs'),
                                    use_proxy=self.get_option('use_proxy'),
                                    url_username=self.get_option('username'),
                                    url_password=self.get_option('password'),
                                    headers=headers,
                                    force_basic_auth=force_basic_auth,
                                    )
            if error is None:
                break
            time.sleep(self.get_option('sleep'))
            iretries += 1

        content = {}

        if response is not None:
            body = to_text(response.read(), 'utf-8')
            if body:
                try:
                    content = json.loads(body)
                except ValueError as e:
                    content['content'] = body

        if error is not None:
            info['error'] = error

        return info, content


    def fetch_url(self, url, validate_certs=None, use_proxy=None, url_username=None, url_password=None, headers=None, force_basic_auth=None):
        """
        Execute base open_url

        """
        error = None
        response = None
        info = dict(url=url, status=-1)
        try:
            response = open_url(url,
                                validate_certs=validate_certs,
                                use_proxy=use_proxy,
                                url_username=url_username,
                                url_password=url_password,
                                headers=headers,
                                force_basic_auth=force_basic_auth,
                                )

            info.update(dict((k.lower(), v) for k, v in response.info().items()))
            info.update(dict(msg="OK (%s bytes)" % response.headers.get('Content-Length', 'unknown'), status=response.code))

        except HTTPError as e:
            try:
                body = e.read()
            except AttributeError:
                body = ''
            error = AnsibleError("Received HTTP error for %s : %s" % (url, to_native(e)))
            info.update({'msg': to_native(e), 'body': body, 'status': e.code})
        except URLError as e:
            error = AnsibleError("Failed lookup url for %s : %s" % (url, to_native(e)))
            info.update(dict(msg="Request failed: %s" % to_native(e), status=int(getattr(e, 'code', -1))))
        except SSLValidationError as e:
            error = AnsibleError("Error validating the server's certificate for %s: %s" % (url, to_native(e)))
        except ConnectionError as e:
            error = AnsibleError("Error connecting to %s: %s" % (url, to_native(e)))
        except Exception as e:        
            error = "Error"
            info.update(dict(msg="An unknown error occurred: %s" % to_native(e), status=-1))

        return response, error, info
    