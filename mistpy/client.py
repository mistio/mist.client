import json

from time import time

from mistpy.helpers import RequestsHandler
from mistpy.helpers import parse_conf_file


class MistClient(object):
    """

    """
    def __init__(self, mist_uri="https://mist.io", email=None, password=None):
        self.uri = mist_uri
        self.email = email
        self.password = password
        self.api_token = None
        self.user_details = None

        self.__init_configure()

        if self.email and self.password:
            self.__authenticate()

    def __init_configure(self):
        if (not self.email) and (not self.password):
            credentials = parse_conf_file()
            self.email = credentials['EMAIL']
            self.password = credentials['PASSWORD']

    def __authenticate(self):
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
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    def supported_providers(self):
        req = self.request(self.uri+'/providers')
        providers = req.get().json()
        supported_providers = providers['supported_providers']
        return supported_providers

    def list_backends(self):
        req = self.request(self.uri+'/backends')
        backends = req.get().json()
        return backends

    def add_backend(self, title, provider, key, secret, tenant_name=None, region=None, apiurl=None, machine_ip=None,
                    machine_key=None, machine_user=None, compute_endpoint=None, machine_port=None):
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
        if response.ok:
            return response
        else:
            return response.status_code

    def delete_backend(self, backend_id):
        req = self.request(self.uri + '/backends/' +backend_id)
        response = req.delete()
        if response.ok:
            return response
        else:
            return response.status_code

    def rename_backend(self, backend_id, new_name):
        payload = {
            'new_name': new_name
        }

        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id, data=data)
        response = req.put()
        if response.ok:
            return response
        else:
            return response.status_code

    def toggle_backend(self, backend_id, new_state):
        payload = {
            'newState': str(new_state)
        }
        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id, data=data)
        response = req.post()
        if response.ok:
            return response
        else:
            return response.status_code

    def list_sizes(self, backend_id):
        req = self.request(self.uri+'/backends/'+backend_id+'/sizes')
        sizes = req.get().json()
        return sizes

    def list_locations(self, backend_id):
        req = self.request(self.uri+'/backends/'+backend_id+'/locations')
        locations = req.get().json()
        return locations

    def list_keys(self):
        req = self.request(self.uri+'/keys')
        keys = req.get().json()
        return keys

    def add_key(self, key_name, private):
        payload = {
            'id': key_name,
            'priv': private
        }

        data = json.dumps(payload)

        req = self.request(self.uri+'/keys', data=data)
        response = req.put()

        if response.ok:
            return response
        else:
            return response.status_code

    def delete_key(self, key_id):
        req = self.request(self.uri+'/keys/'+key_id)
        response = req.delete()
        if response.ok:
            return response
        else:
            return response.status_code

    def list_images(self, backend_id):
        req = self.request(self.uri+'/backends/'+backend_id+'/images')
        images = req.get().json()
        return images

    def search_image(self, backend_id, search_term):
        payload = {
            'search_term': search_term
        }
        data = json.dumps(payload)

        req = self.request(self.uri+'/backends/'+backend_id+'/images', data=data)
        images = req.get().json()
        return images

    def list_machines(self, backend_id, filtered=None):
        req = self.request(self.uri+'/backends/'+backend_id+'/machines')
        all_machines = req.get().json()
        machines = []

        if filtered == "running":
            for machine in all_machines:
                if machine['state'] == 'running':
                    machines.append(machine)
        else:
            machines = all_machines
        return machines

    def create_machine(self, backend_id, name, key_id, image_id, location_id, size_id, image_extra="", disk=""):
        payload = {
            'name': name,
            'key': key_id,
            'image': image_id,
            'location': location_id,
            'size': size_id,
            'image_extra': image_extra,
            'disk': disk
        }
        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id+'/machines', data=data)
        response = req.post()
        if response.ok:
            return response
        else:
            return response.status_code

    def machine_actions(self, backend_id, machine_id, action):
        payload = {
            'action': action
        }
        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id, data=data)
        response = req.post()
        if response.ok:
            return response
        else:
            return response.status_code

    def toggle_monitoring(self, backend_id, machine_id, machine_name, public_ips, dns_name, action='enable'):
        payload = {
            'action': action,
            'name': machine_name,
            'public_ips': public_ips,
            'dns_name': dns_name
        }
        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id+'/monitoring', data=data)
        response = req.post()
        if response.ok:
            return response
        else:
            return response.status_code

    def get_stats(self, backend_id, machine_id, start=int(time()), stop=int(time())+10, step=10):
        payload = {
            'start': start,
            'stop': stop,
            'step': step
        }

        data = json.dumps(payload)
        req = self.request(self.uri+'/backends/'+backend_id+'/machines/'+machine_id+'/stats', data=data)
        stats = req.get().json()
        return stats
