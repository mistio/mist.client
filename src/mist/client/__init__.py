import json

from mist.client.helpers import RequestsHandler
from mist.client.model import Backend, Key


class MistClient(object):
    """

    """
    def __init__(self, mist_uri="https://mist.io", email=None, password=None):
        """
        Initialize the mist.client. In case email and password are given, it will try to authenticate with mist.io
        and keep the api_token that is returned to be used with the later requests.


        :param mist_uri: By default it is 'https://mist.io'. Can be changed if there's a different installation of
        mist.io
        :param email: Email to authenticate with mist.io. May be left 'None' if there's a standalone installation of
        mist.io that does not require authentication.
        :param password: Password to authenticate with mist.io. May be left 'None' if there's a standalone installation
        of mist.io that does not require authentication.
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

        :returns: An instance of RequestsHandler
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

        Populates self.backends dict with mist.client.model.Backend instances

        :returns: A list of the added backends' names
        """
        req = self.request(self.uri+'/backends')
        backends = req.get().json()
        if backends:
            for backend in backends:
                self._backends[backend['title']] = Backend(backend, self)
        else:
            self._backends = {}

    @property
    def backends(self):
        if self._backends is None:
            self._backends = {}
            self._list_backends()

        return self._backends

    def update_backends(self):
        self._backends = {}
        self._list_backends()
        return self._backends

    def add_backend(self, title, provider, key, secret, tenant_name=None, region=None, apiurl=None, machine_ip=None,
                    machine_key=None, machine_user=None, compute_endpoint=None, machine_port=None):
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
        :returns: Updates self.backends dict and returns a list of added backends' names.
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
            'machine_port': machine_port
        }

        req = self.request(self.uri+'/backends', data=json.dumps(payload))
        response = req.post()
        self.update_backends()
        return

    def _list_keys(self):
        req = self.request(self.uri+'/keys')
        keys = req.get().json()
        if keys:
            self._keys = {}
            for key in keys:
                self._keys[key['id']] = Key(key, self)
        else:
            self._keys = {}
        return keys

    @property
    def keys(self):
        if self._keys is None:
            self._keys = {}
            self._list_keys()

        return self._keys

    # def add_key(self, key_name, private):
    #     payload = {
    #         'id': key_name,
    #         'priv': private
    #     }
    #
    #     data = json.dumps(payload)
    #
    #     req = self.request(self.uri+'/keys', data=data)
    #     response = req.put()
    #
    #     if response.ok:
    #         return response
    #     else:
    #         return response.status_code
    #
    # def delete_key(self, key_id):
    #     req = self.request(self.uri+'/keys/'+key_id)
    #     response = req.delete()
    #     if response.ok:
    #         return response
    #     else:
    #         return response.status_code
    #
    #
    # def create_machine(self, backend_id, name, key_id, image_id, location_id, size_id, image_extra="", disk=""):
    #     payload = {
    #         'name': name,
    #         'key': key_id,
    #         'image': image_id,
    #         'location': location_id,
    #         'size': size_id,
    #         'image_extra': image_extra,
    #         'disk': disk
    #     }
    #     data = json.dumps(payload)
    #     req = self.request(self.uri+'/backends/'+backend_id+'/machines', data=data)
    #     response = req.post()
    #     if response.ok:
    #         return response
    #     else:
    #         return response.status_code
    #
    # def machine_actions(self, backend_id, machine_id, action):
    #     payload = {
    #         'action': action
    #     }
    #     data = json.dumps(payload)
    #     req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id, data=data)
    #     response = req.post()
    #     if response.ok:
    #         return response
    #     else:
    #         return response.status_code
    #
    # def toggle_monitoring(self, backend_id, machine_id, machine_name, public_ips, dns_name, action='enable'):
    #     payload = {
    #         'action': action,
    #         'name': machine_name,
    #         'public_ips': public_ips,
    #         'dns_name': dns_name
    #     }
    #     data = json.dumps(payload)
    #     req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id+'/monitoring', data=data)
    #     response = req.post()
    #     if response.ok:
    #         return response
    #     else:
    #         return response.status_code
    #
    # def get_stats(self, backend_id, machine_id, start=int(time()), stop=int(time())+10, step=10):
    #     payload = {
    #         'start': start,
    #         'stop': stop,
    #         'step': step
    #     }
    #
    #     data = json.dumps(payload)
    #     req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id+'/stats', data=data)
    #     stats = req.get().json()
    #     return stats
