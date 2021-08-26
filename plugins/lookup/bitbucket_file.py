# Copyright: (c) 2021, Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
    name: bitbucket_file
    author: Krzysztof Lewandowski <krzysztof.lewandowski@nordea.com>
    version_added: 1.0.0
    short_description: Read file contents from Bitbucket Server
    description:
      - Returns a list of strings.
      - For each file in the list of files you pass in, returns a string containing a base64-encoded blob contents of the file from Bitbucket Server.
    options:
      _terms:
        description: Path(s) of file(s) on the Bitbucket Server to fetch content from.
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
      unvault:
        description:
        - If C(yes), read vaulted file(s) contents and decrypt it.
        type: bool
        default: no
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
      - This module returns an 'in memory' base64 encoded version of the file, take
        into account that this will require at least twice the RAM as the original file size.
'''

EXAMPLES = """
- name: Display file contents
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_file', 'path/to/baz.yml', 
             project_key='FOO', repository='bar', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret') 
             | b64decode
             | from_yaml }}"  


- name: Display multiple files contents
  ansible.builtin.debug:
    msg: "{{ item | b64decode }}"
  loop: "{{ query('esp.bitbucket.bitbucket_file', 'path/to/baz.yml', 'qux.json',
            project_key='FOO', repository='bar', at='master', validate_certs='no', 
            url='https://bitbucket.example.com', token='MjA2M...hqP58' ) }}"
  loop_control:
    label: "[Processing a file from Bitbucket Server ..]"

- name: lookup | Read vaulted file, do not decrypt it
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_file', 'path/to/vault.yml', 
             project_key='FOO', repository='bar', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret', unvault='no' ) 
             | b64decode
             | from_yaml }}" 

- name: lookup | Read vaulted file, decrypt it
  ansible.builtin.debug:
    msg: "{{ lookup('esp.bitbucket.bitbucket_file', 'path/to/vault.yml', 
             project_key='FOO', repository='bar', validate_certs='no', 
             url='https://bitbucket.example.com', username='SVCxxxxxx', password='secret', unvault='yes' ) 
             | b64decode
             | from_yaml }}" 
"""

RETURN = """
  _raw:
    description:
      - content of file(s)
    type: list
    elements: str
"""

import base64
import json
import urllib
import time
import tempfile

import requests
from requests.auth import HTTPBasicAuth

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.urls import basic_auth_header
from ansible_collections.esp.bitbucket.plugins.module_utils.bitbucket import BitbucketHelper

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        self.set_options(var_options=variables, direct=kwargs)

        ret = []

        try:
            for term in terms:

                force_basic_auth = True
                headers = {}
                if self.get_option('token') is not None:
                    headers.update({
                        'Authorization': 'Bearer {0}'.format(self.get_option('token')),
                    })
                    force_basic_auth = False

                at = ""
                if self.get_option('at') is not None:
                    at = "?at=%s" % self.get_option('at')

                if self.get_option('url') is None:
                    api_url = BitbucketHelper.BITBUCKET_API_URL
                else:
                  api_url = self.get_option('url')
                url = BitbucketHelper.BITBUCKET_API_ENDPOINTS['repos-raw-path'].format(
                                            url=api_url,
                                            projectKey=self.get_option('project_key'),
                                            repositorySlug=self.get_option('repository'),
                                            path=term,
                                            at=at,
                )

                iretries = 1
                while iretries <= self.get_option('retries'):
                    response, error = self.request(url, 
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
   
                if (self.get_option('unvault') is not None) and (self.get_option('unvault')):    
                    ff = tempfile.NamedTemporaryFile()
                    ff.write(response.read())
                    ff.seek(0)                
                    actual_file = self._loader.get_real_file(ff.name, decrypt=True)
                    with open(actual_file, 'rb') as f:
                        b_contents = f.read()                    
                    ret.append(to_text(base64.b64encode(b_contents)))
                    ff.close()
                else:
                    ret.append(to_text(base64.b64encode(response.read())))                    

        except Exception as e:
            raise AnsibleError(
                "Error locating '%s' in Bitbucket Server. Error was %s" % (term, e))

        return ret


    def request(self, url, validate_certs=None, use_proxy=None, url_username=None, url_password=None, headers=None, force_basic_auth=None):

        error = None
        response = None
        try:
            response = open_url(url, 
                                validate_certs=validate_certs,
                                use_proxy=use_proxy,
                                url_username=url_username,
                                url_password=url_password,
                                headers=headers,
                                force_basic_auth=force_basic_auth,
                                )
        except HTTPError as e:
            error = AnsibleError("Received HTTP error for %s : %s" % (url, to_native(e)))
        except URLError as e:
            error = AnsibleError("Failed lookup url for %s : %s" % (url, to_native(e)))
        except SSLValidationError as e:
            error = AnsibleError("Error validating the server's certificate for %s: %s" % (url, to_native(e)))
        except ConnectionError as e:
            error = AnsibleError("Error connecting to %s: %s" % (url, to_native(e)))
        except:
            error = "Error"

        return response, error
    