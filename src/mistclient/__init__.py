import json

from mistclient.helpers import RequestsHandler
from mistclient.model import Backend, Key


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
        self._machines = None
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
        req = self.request(self.uri+'/providers', api_version=2)
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

    def backends(self, id=None, name=None, provider=None, search=None):
        """
        Property-like function to call the _list_backends function in order to populate self._backends dict

        :returns: A list of Backend instances.
        """
        if self._backends is None:
            self._backends = {}
            self._list_backends()

        if id:
            return [self._backends[backend_id] for backend_id in self._backends.keys()
                    if id == self._backends[backend_id].id]
        elif name:
            return [self._backends[backend_id] for backend_id in self._backends.keys()
                    if name == self._backends[backend_id].title]
        elif provider:
            return [self._backends[backend_id] for backend_id in self._backends.keys()
                    if provider == self._backends[backend_id].provider]
        elif search:
            return [self._backends[backend_id] for backend_id in self._backends.keys()
                    if search in self._backends[backend_id].title
                    or search in self._backends[backend_id].id
                    or search in self._backends[backend_id].provider]
        else:
            return [self._backends[backend_id] for backend_id in self._backends.keys()]

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

    def add_backend(self, title, provider, **kwargs):
        payload = {}
        if provider == "ec2":
            payload = self._add_backend_ec2(**kwargs)
        elif provider == "rackspace":
            payload = self._add_backend_rackspace(**kwargs)
        elif provider == "nephoscale":
            payload = self._add_backend_nephoscale(**kwargs)
        elif provider == "softlayer":
            payload = self._add_backend_softlayer(**kwargs)
        elif provider == "digitalocean":
            payload = self._add_backend_digitalocean(**kwargs)
        elif provider == "gce":
            payload = self._add_backend_gce(**kwargs)
        elif provider == "azure":
            payload = self._add_backend_azure(**kwargs)
        elif provider == "linode":
            payload = self._add_backend_linode(**kwargs)
        elif provider == "bare_metal":
            payload = self._add_backend_bare_metal(**kwargs)
        elif provider in ['vcloud', 'indonesian_vcloud']:
            payload = self._add_backend_vcloud(**kwargs)
        elif provider == "docker":
            payload = self._add_backend_docker(**kwargs)
        elif provider == "libvirt":
            payload = self._add_backend_libvirt(**kwargs)
        elif provider == "hpcloud":
            payload = self._add_backend_hp(**kwargs)
        elif provider == "openstack":
            payload = self._add_backend_openstack(**kwargs)

        payload['title'] = title
        payload['provider'] = provider
        req = self.request(self.uri+'/backends', data=json.dumps(payload), api_version=2)
        response = req.post()
        self.update_backends()
        return

    def _add_backend_rackspace(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'api_key': kwargs.get('api_key', ''),
            'region': kwargs.get('region', '')
        }
        return payload

    def _add_backend_ec2(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', ''),
            'api_secret': kwargs.get('api_secret', ''),
            'region': kwargs.get('region', '')
        }
        return payload

    def _add_backend_nephoscale(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', '')
        }
        return payload

    def _add_backend_softlayer(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_backend_digitalocean(self, **kwargs):
        payload = {
            'token': kwargs.get('token', '')
        }
        return payload

    def _add_backend_gce(self, **kwargs):
        payload = {
            'email': kwargs.get('email', ''),
            'private_key': kwargs.get('private_key', ''),
            'project_id': kwargs.get('project_id', '')
        }
        return payload

    def _add_backend_azure(self, **kwargs):
        payload = {
            'subscription_id': kwargs.get('subscription_id', ''),
            'certificate': kwargs.get('certificate', '')
        }
        return payload

    def _add_backend_linode(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_backend_bare_metal(self, **kwargs):
        payload = {
            'machine_ip': kwargs.get('machine_ip', ''),
            'machine_key': kwargs.get('machine_key', ''),
            'machine_user': kwargs.get('machine_user', 'root'),
            'machine_port': kwargs.get('machine_port', 22)
        }
        return payload

    def _add_backend_vcloud(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'organization': kwargs.get('organization', ''),
            'host': kwargs.get('host', '')
        }
        return payload

    def _add_backend_docker(self, **kwargs):
        payload = {
            'docker_port': int(kwargs.get('docker_port', 4243)),
            'docker_host': kwargs.get('docker_host', ''),
            'auth_user': kwargs.get('auth_user', ''),
            'auth_password': kwargs.get('auth_password', ''),
            'key_file': kwargs.get('key_file', ''),
            'cert_file': kwargs.get('cert_file', '')
        }
        return payload

    def _add_backend_libvirt(self, **kwargs):
        payload = {
            'machine_hostname': kwargs.get('machine_hostname', ''),
            'machine_user': kwargs.get('machine_user', 'root'),
            'machine_key': kwargs.get('machine_key', '')
        }
        return payload

    def _add_backend_hp(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'tenant_name': kwargs.get('tenant_name', ''),
            'region': kwargs.get('region', '')
        }
        return payload

    def _add_backend_openstack(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'auth_url': kwargs.get('auth_url', ''),
            'tenant_name': kwargs.get('tenant_name', ''),
            'region': kwargs.get('region', ''),
            'compute_endpoint': kwargs.get('compute_endpoint', '')
        }
        return payload

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

    def keys(self, id=None, search=None):
        """
        Property-like function to call the _list_keys function in order to populate self._keys dict

        :returns: A list of Key instances
        """
        if self._keys is None:
            self._keys = {}
            self._list_keys()

        if id:
            return [self._keys[key_id] for key_id in self._keys.keys()
                    if id == self._keys[key_id].id]
        elif search:
            return [self._keys[key_id] for key_id in self._keys.keys()
                    if search in self._keys[key_id].id]
        else:
            return [self._keys[key_id] for key_id in self._keys.keys()]

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

    def _list_machines(self):
        self._machines = []
        for backend in self.backends():
            machines = backend.machines()
            for machine in machines:
                self._machines.append(machine)

    def machines(self, id=None, name=None, search=None):
        if self._machines is None:
            self._list_machines()

        if id:
            return [machine for machine in self._machines if machine.id == id]
        elif name:
            return [machine for machine in self._machines if machine.name == name]
        elif search:
            return [machine for machine in self._machines
                    if search in machine.id or search in machine.name]
        else:
            return self._machines