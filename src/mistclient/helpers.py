import sys
import json

import time

from HTMLParser import HTMLParser as _HTMLParser
from HTMLParser import HTMLParseError

try:
    import requests
except ImportError:
    print "requests required for this module'"
    sys.exit(1)


class RequestsHandler(object):
    """
    A wrapper-like class to be used with all the requests being made to
    mist.io service.
    """

    def __init__(self, mist_uri, data=None, api_token=None, timeout=None,
                 api_version=None, verify=True):
        """

        :param mist_uri: The uri to make the requests to.
        :param data: Json object with all the params needed by some requests.
        :param api_token: If api_token is used, then you do not have to provide
        username and password.
        :param timeout: Optional. If given the request will fail if it lasts
        longer than the timeout.

        :returns: A RequestsHandler instance.
        """
        self.headers = {'Authorization': api_token}
        if api_version:
            self.headers['Api-Version'] = api_version
        self.uri = mist_uri
        self.data = data
        self.timeout = timeout
        self.verify = verify

    def response(self, resp):
        """
        For each respone we check if the response status is ok, otherwise raise
        an error with the the response's content.
        :param resp: The response we got after a request.
        :return: Return the response if response.ok, otherwise raise error with
        the response.content.
        """
        if resp.ok:
            return resp
        else:
            raise Exception(resp.content)

    def post(self):
        resp = requests.post(self.uri, data=self.data, headers=self.headers,
                             timeout=self.timeout, verify=self.verify)
        return self.response(resp)

    def get(self):
        resp = requests.get(self.uri, data=self.data, headers=self.headers,
                            timeout=self.timeout, verify=self.verify)
        return self.response(resp)

    def put(self):
        resp = requests.put(self.uri, data=self.data, headers=self.headers,
                            timeout=self.timeout, verify=self.verify)
        return self.response(resp)

    def delete(self):
        resp = requests.delete(self.uri, data=self.data, headers=self.headers,
                               timeout=self.timeout, verify=self.verify)
        return self.response(resp)


class HTMLParser(_HTMLParser):

    _handle_req = False

    def __init__(self, html_data):
        _HTMLParser.__init__(self)
        self.user_info = {}
        if html_data:
            self.feed(html_data)

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and not attrs:
            self._handle_req = True

    def handle_endtag(self, tag):
        if tag == 'script' and self._handle_req:
            self._handle_req = False

    def handle_data(self, data):
        if self._handle_req:
            if str(data).startswith(' var '):
                _data = data.lstrip(' var ').split('=')
                key, value = _data[0], json.loads(_data[1])
                if not isinstance(value, basestring) and \
                        not isinstance(value, list) and \
                        not isinstance(value, dict):
                    pass
                else:
                    self.user_info[key] = value

    def user_details(self):
        user = {}
        for key in ['FIRST_NAME', 'LAST_NAME', 'EMAIL',
                    'NUMBER_OF_SERVERS', 'COMPANY_NAME']:
            if key in self.user_info.keys():
                user[key] = self.user_info[key]
        return user

    def plan_details(self):
        current = self.user_info['CURRENT_PLAN']
        plan = {}
        for key in ['title', 'started', 'expiration', 'machine_limit']:
            if key in ['started', 'expiration']:
                current[key] = time.ctime(current[key])
            plan[key.upper()] = current[key]
        return plan


def machine_from_id(cloud, id):
    machines = cloud.machines
    for key in machines.keys():
        machine = machines[key]
        if id == machine.id:
            return machine
    return None


def cloud_from_id(client, id):
    clouds = client.clouds
    for key in clouds.keys():
        cloud = clouds[key]
        if id == cloud.id:
            return cloud
    return
