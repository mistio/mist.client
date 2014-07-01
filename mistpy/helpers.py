import sys
import os
import yaml

try:
    import requests
except ImportError:
    print "requests required for this module'"
    sys.exit(1)


class RequestsHandler(object):
    """

    """

    def __init__(self, mist_uri, data=None, api_token=None, timeout=None):
        self.headers = {'Authorization': api_token}
        self.uri = mist_uri
        self.data = data
        self.timeout = timeout

    def post(self):
        response = requests.post(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return response

    def get(self):
        response = requests.get(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return response

    def put(self):
        response = requests.put(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return response

    def delete(self):
        response = requests.delete(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return response


def parse_conf_file():
    home_dir = os.getenv("HOME")
    if os.path.isfile(home_dir+"/.mist.conf"):
        config = open(home_dir+"/.mist.conf", 'r')
        credentials = yaml.load(config)
        if credentials:
            return credentials

    credentials = dict()
    credentials['EMAIL'] = None
    credentials['PASSWORD'] = None
    return credentials