import sys

try:
    import requests
except ImportError:
    print "requests required for this module'"
    sys.exit(1)


class RequestsHandler(object):
    """

    """

    def __init__(self, mist_uri, data=None, api_token=None, timeout=None):
        """

        :param mist_uri:
        :param data:
        :param api_token:
        :param timeout:
        :return:
        """
        self.headers = {'Authorization': api_token}
        self.uri = mist_uri
        self.data = data
        self.timeout = timeout

    def response(self, resp):
        if resp.ok:
            return resp
        else:
            raise Exception(resp.content)

    def post(self):
        resp = requests.post(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return self.response(resp)

    def get(self):
        resp = requests.get(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return self.response(resp)

    def put(self):
        resp = requests.put(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return self.response(resp)

    def delete(self):
        resp = requests.delete(self.uri, data=self.data, headers=self.headers, timeout=self.timeout)
        return self.response(resp)

