from mist.client.helpers import RequestsHandler


class Backend(object):
    """

    """
    def __init__(self, backend, api_token=None):
        self.title = backend['title']
        self.id = backend['id']
        self.enabled = backend['enabled']
        self.provider = backend['provider']
        self.api_token = api_token

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)