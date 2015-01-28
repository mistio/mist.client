import sys

try:
    import requests
except ImportError:
    print "requests required for this module'"
    sys.exit(1)


class RequestsHandler(object):
    """
    A wrapper-like class to be used with all the requests being made to mist.io service.
    """

    def __init__(self, mist_uri, data=None, api_token=None, timeout=None, api_version=None):
        """

        :param mist_uri: The uri to make the requests to.
        :param data: Json object with all the params needed by some requests.
        :param api_token: If api_token is used, then you do not have to provide username and password.
        :param timeout: Optional. If given the request will fail if it lasts longer than the timeout.

        :returns: A RequestsHandler instance.
        """
        self.headers = {'Authorization': api_token}
        if api_version:
            self.headers['Api-Version'] = api_version
        self.uri = mist_uri
        self.data = data
        self.timeout = timeout

    def response(self, resp):
        """
        For each respone we check if the response status is ok, otherwise raise an error with the the response's
        content.
        :param resp: The response we got after a request.
        :return: Return the response if response.ok, otherwise raise error with the response.content.
        """
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


def machine_from_id(backend, id):
    machines = backend.machines
    for key in machines.keys():
        machine = machines[key]
        if id == machine.id:
            return machine
    return None


def backend_from_id(client, id):
    backends = client.backends
    for key in backends.keys():
        backend = backends[key]
        if id == backend.id:
            return backend
    return