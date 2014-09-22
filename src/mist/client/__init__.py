import json

from mist.client.helpers import RequestsHandler
from mist.client.model import Backend, Key


class MistClient(object):
    """
    The base class that initiates a new client that connects with mist.io service.
    """
    def __init__(self, mist_uri="https://mist.io", email=None, password=None):
        """
        Initialize the mist.client. In case email and password are given, it will try to authenticate with mist.io
        and keep the api_token that is returned to be used with the later requests.


        :param mist_uri: By default it is 'https://mist.io'. Can be changed if there's a different installation of mist.io
        :param email: Email to authenticate with mist.io. May be left 'None' if there's a standalone installation of mist.io that does not require authentication.
        :param password: Password to authenticate with mist.io. May be left 'None' if there's a standalone installation of mist.io that does not require authentication.
        """
        self.uri = mist_uri
        self.email = email
        self.password = password
        self.api_token = None
        self.user_details = None

        self._backends = None
        self._keys = None

        if self.email and self.password:
            self.__authenticate()

    def __authenticate(self):
        """
        Sends a json payload with the email and password in order to get the authentication api_token to be used with
        the rest of the requests
        """
        payload = {
            'email': self.email,
            'password': self.password
        }

        data = json.dumps(payload)
        req = self.request(self.uri+'/auth', data=data)
        response = req.post().json()
        token = response['mist_api_token']
        self.api_token = "mist_1 %s:%s" % (self.email, token)
        self.user_details = response

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of mist.client.helpers.RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    @property
    def supported_providers(self):
        """
        Request a list of all available providers

        :returns: A list of all available providers (e.g. {'provider': 'ec2_ap_northeast', 'title': 'EC2 AP NORTHEAST'})
        """
        req = self.request(self.uri+'/providers')
        providers = req.get().json()
        supported_providers = providers['supported_providers']
        return supported_providers

    def _list_backends(self):
        """
        Request a list of all added backends.

        Populates self._backends dict with mist.client.model.Backend instances
        """
        req = self.request(self.uri+'/backends')
        backends = req.get().json()
        if backends:
            for backend in backends:
                self._backends[backend['id']] = Backend(backend, self)
        else:
            self._backends = {}

    @property
    def backends(self):
        """
        Property-like function to call the _list_backends function in order to populate self._backends dict

        :returns: A list of Backend instances.
        """
        if self._backends is None:
            self._backends = {}
            self._list_backends()

        return self._backends

    def backend_from_id(self, backend_id):
        self.backends
        if backend_id in self._backends.keys():
            return self._backends[backend_id]
        else:
            return None

    def backend_from_title(self, backend_title):
        self.backends
        for key in self._backends.keys():
            backend = self._backends[key]
            if backend_title == backend.title:
                return backend

        return None

    def backend_from_provider(self, backend_provider):
        self.backends
        for key in self._backends.keys():
            backend = self._backends[key]
            if backend_provider == backend.provider:
                return backend

        return None

    def search_backend(self, backend_key):
        """
        Choose a backend by providing a backend's id, title or provider
        """
        self.backends
        backend = self.backend_from_id(backend_key)
        if backend:
            return backend

        backend = self.backend_from_title(backend_key)
        if backend:
            return backend

        backend = self.backend_from_provider(backend_key)
        if backend:
            return backend

    def update_backends(self):
        """
        Update added backends' info and re-populate the self._backends dict.

        This one is used whenever a new backend is added, renamed etc etc or whenever you want to update the list
        of added backends.

        :returns: A list of Backend instances.
        """
        self._backends = {}
        self._list_backends()
        return self._backends

    def add_backend(self, title, provider, key, secret, tenant_name=None, 
                    region=None, apiurl=None, machine_ip=None, machine_key=None, 
                    machine_user=None, compute_endpoint=None, machine_port=None,
                    remove_on_error=True):
        """
        Add a backend (hint: run supported_providers first in order to see all the available options)

        :param title: Title of the backend
        :param provider: A provider's name (must be one of the list of supported_providers)
        :param key: According to each provider can be a username, a api_key etc.
        :param secret: According to each provider can be a simple password, a api_secret etc.
        :param tenant_name: Used if needed for OpenStack backends.
        :param region: Necessary only if there is a custom Openstack region.
        :param apiurl: APIURL needed by Openstack and HP Cloud.
        :param machine_ip: Ip address needed when adding Bare Metal Server.
        :param machine_key: Id of ssh key needed when adding Bare Metal Server. The key must have been added first.
        :param machine_user: User for Bare Metal Server.
        :param compute_endpoint: Needed by some OpenStack installations.
        :param machine_port: Used when adding a Bare Metal Server
        :returns: Updates self._backends dict.

        """
        payload = {
            'title': title,
            'provider': provider,
            'apikey': key,
            'apisecret': secret,
            'tenant_name': tenant_name,
            'region': region,
            'apiurl': apiurl,
            'machine_ip': machine_ip,
            'machine_key': machine_key,
            'machine_user': machine_user,
            'compute_endpoint': compute_endpoint,
            'machine_port': machine_port,
            'remove_on_error': remove_on_error
        }

        req = self.request(self.uri+'/backends', data=json.dumps(payload))
        response = req.post()
        self.update_backends()
        return

    def _list_keys(self):
        """
        Retrieves a list of all added Keys and populates the self._keys dict with Key instances

        :returns: A list of Keys instances
        """
        req = self.request(self.uri+'/keys')
        keys = req.get().json()
        if keys:
            self._keys = {}
            for key in keys:
                self._keys[key['id']] = Key(key, self)
        else:
            self._keys = {}

    @property
    def keys(self):
        """
        Property-like function to call the _list_keys function in order to populate self._keys dict

        :returns: A list of Key instances
        """
        if self._keys is None:
            self._keys = {}
            self._list_keys()

        return self._keys

    def update_keys(self):
        """
        Update added keys' info and re-populate the self._keys dict.

        This one is used whenever a new key is added, renamed etc etc or whenever you want to update the list
        of added keys.

        :returns: A list of Key instances.
        """
        self._keys = {}
        self._list_keys()
        return self._keys

    def generate_key(self):
        """
        Ask mist.io to randomly generate a private ssh-key to be used with the creation of a new Key

        :returns: A string of a randomly generated ssh private key
        """
        req = self.request(self.uri+"/keys")
        private_key = req.post().json()
        return private_key['priv']

    def add_key(self, key_name, private):
        """
        Add a new key to mist.io

        :param key_name: Name of the new key (it will be used as the key's id as well).
        :param private: Private ssh-key in string format (see also generate_key() ).

        :returns: An updated list of added keys.
        """
        payload = {
            'id': key_name,
            'priv': private
        }

        data = json.dumps(payload)

        req = self.request(self.uri+'/keys', data=data)
        req.put()
        self.update_keys()

