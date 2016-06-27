import json

import sys
from time import sleep

from mistclient.helpers import RequestsHandler, HTMLParser
from mistclient.model import Cloud, Key, Script


class MistClient(object):
    """
    The base class that initiates a new client that connects with mist.io service.
    """

    def __init__(self, mist_uri="https://mist.io", email=None, password=None,
                 api_token=None, verify=True):
        """
        Initialize the mist.client. In case email and password are given, it
        will try to authenticate with mist.io and keep the api_token that is
        returned to be used with the later requests.

        :param mist_uri: By default it is 'https://mist.io'. Can be changed if
        there's a different installation of mist.io
        :param email: Email to authenticate with mist.io. May be left 'None' if
        there's a standalone installation of mist.io that does not require
        authentication.
        :param password: Password to authenticate with mist.io. May be left
        'None' if there's a standalone installation of mist.io that does not
        require authentication.
        """
        if not mist_uri.endswith("/"):
            mist_uri = mist_uri + "/"
        self.uri = mist_uri + "api/v1"
        self.email = email
        self.password = password
        self.api_token = api_token
        self.user_details = None
        self.verify = verify

        self._clouds = None
        self._machines = None
        self._keys = None
        self._scripts = None

        if self.email and self.password:
            self.__authenticate()

    def __authenticate(self):
        """
        Sends a json payload with the email and password in order to get the
        authentication api_token to be used with the rest of the requests
        """
        if self.api_token:
            # verify current API token
            check_auth_uri = self.uri.split('/api/v1')[0] + '/check_token'
            req = self.request(check_auth_uri)
            try:
                ping = req.get().json()
            except Exception as exc:
                if str(exc).startswith('User not authenticated'):
                    self.api_token = None
            else:
                if self.email == ping['hello']:
                    return
                print "Authentication failed"
                sys.exit(1)

        auth_uri = self.uri.split('/api/v1')[0] + '/auth'
        payload = {
            'email': self.email,
            'password': self.password
        }
        data = json.dumps(payload)
        req = self.request(auth_uri, data=data)
        response = req.post().json()
        token = response.get('mist_api_token', None)
        if token:
            # backwards compatibility with old Authentication system
            self.api_token = "mist_1 %s:%s" % (self.email, token)
        else:
            self.api_token = response.get('token', None)

    def user_info(self):
        """
        General user info information as returned in /account in our API
        """
        account_uri = self.uri.split('/api/v1')[0] + '/account'
        req = self.request(account_uri)
        account_info = req.get()
        user_data = HTMLParser(account_info.content)
        return user_data

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the
        api_token and all the other params to the requests that are being made

        :returns: An instance of mist.client.helpers.RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token,
                               verify=self.verify, **kwargs)

    @property
    def supported_providers(self):
        """
        Request a list of all available providers

        :returns: A list of all available providers (e.g. {'provider':
        'ec2_ap_northeast', 'title': 'EC2 AP NORTHEAST'})
        """
        req = self.request(self.uri + '/providers', api_version=2)
        providers = req.get().json()
        supported_providers = providers['supported_providers']
        return supported_providers

    def _list_clouds(self):
        """
        Request a list of all added clouds.

        Populates self._clouds dict with mist.client.model.Cloud instances
        """
        req = self.request(self.uri + '/clouds')
        clouds = req.get().json()
        if clouds:
            for cloud in clouds:
                self._clouds[cloud['id']] = Cloud(cloud, self)
        else:
            self._clouds = {}

    def post_logs(self, entries=[]):
        if not entries:
            return

        payload = {
            'entries': entries,
        }

        data = json.dumps(payload)
        req = self.request(self.uri + '/logs', data=data)
        req.post()

    def clouds(self, id=None, name=None, provider=None, search=None):
        """
        Property-like function to call the _list_clouds function in order to populate self._clouds dict

        :returns: A list of Cloud instances.
        """
        if self._clouds is None:
            self._clouds = {}
            self._list_clouds()

        if id:
            return [self._clouds[cloud_id] for cloud_id in self._clouds.keys()
                    if id == self._clouds[cloud_id].id]
        elif name:
            return [self._clouds[cloud_id] for cloud_id in self._clouds.keys()
                    if name == self._clouds[cloud_id].title]
        elif provider:
            return [self._clouds[cloud_id] for cloud_id in self._clouds.keys()
                    if provider == self._clouds[cloud_id].provider]
        elif search:
            return [self._clouds[cloud_id] for cloud_id in self._clouds.keys()
                    if search in self._clouds[cloud_id].title
                    or search in self._clouds[cloud_id].id
                    or search in self._clouds[cloud_id].provider]
        else:
            return [self._clouds[cloud_id] for cloud_id in self._clouds.keys()]

    def update_clouds(self):
        """
        Update added clouds' info and re-populate the self._clouds dict.

        This one is used whenever a new cloud is added, renamed etc etc or whenever you want to update the list
        of added clouds.

        :returns: A list of Cloud instances.
        """
        self._clouds = {}
        self._list_clouds()
        return self._clouds

    def add_cloud(self, title, provider, **kwargs):
        payload = {}
        if provider == "ec2":
            payload = self._add_cloud_ec2(**kwargs)
        elif provider == "rackspace":
            payload = self._add_cloud_rackspace(**kwargs)
        elif provider == "nephoscale":
            payload = self._add_cloud_nephoscale(**kwargs)
        elif provider == "softlayer":
            payload = self._add_cloud_softlayer(**kwargs)
        elif provider == "digitalocean":
            payload = self._add_cloud_digitalocean(**kwargs)
        elif provider == "gce":
            payload = self._add_cloud_gce(**kwargs)
        elif provider == "azure":
            payload = self._add_cloud_azure(**kwargs)
        elif provider == "linode":
            payload = self._add_cloud_linode(**kwargs)
        elif provider == "bare_metal":
            payload = self._add_cloud_bare_metal(**kwargs)
        elif provider == "coreos":
            payload = self._add_cloud_coreos(**kwargs)
        elif provider in ['vcloud', 'indonesian_vcloud']:
            payload = self._add_cloud_vcloud(**kwargs)
        elif provider == 'vsphere':
            payload = self._add_cloud_vsphere(**kwargs)
        elif provider == "docker":
            payload = self._add_cloud_docker(**kwargs)
        elif provider == "libvirt":
            payload = self._add_cloud_libvirt(**kwargs)
        # elif provider == "hpcloud":
        #     payload = self._add_cloud_hp(**kwargs)
        elif provider == "openstack":
            payload = self._add_cloud_openstack(**kwargs)
        elif provider == "hostvirtual":
            payload = self._add_cloud_hostvirtual(**kwargs)
        elif provider == "vultr":
            payload = self._add_cloud_vultr(**kwargs)
        elif provider == "packet":
            payload = self._add_cloud_packet(**kwargs)

        payload['title'] = title
        payload['provider'] = provider
        req = self.request(self.uri + '/clouds',
                           data=json.dumps(payload), api_version=2)
        response = req.post()
        self.update_clouds()
        return

    def _add_cloud_rackspace(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'api_key': kwargs.get('api_key', ''),
            'region': kwargs.get('region', '')
        }
        return payload

    def _add_cloud_ec2(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', ''),
            'api_secret': kwargs.get('api_secret', ''),
            'region': kwargs.get('region', '')
        }
        return payload

    def _add_cloud_nephoscale(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', '')
        }
        return payload

    def _add_cloud_softlayer(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_cloud_digitalocean(self, **kwargs):
        payload = {
            'token': kwargs.get('token', '')
        }
        return payload

    def _add_cloud_gce(self, **kwargs):
        payload = {
            'email': kwargs.get('email', ''),
            'private_key': kwargs.get('private_key', ''),
            'project_id': kwargs.get('project_id', '')
        }
        return payload

    def _add_cloud_azure(self, **kwargs):
        payload = {
            'subscription_id': kwargs.get('subscription_id', ''),
            'certificate': kwargs.get('certificate', '')
        }
        return payload

    def _add_cloud_linode(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_cloud_bare_metal(self, **kwargs):
        payload = {
            'machine_ip': kwargs.get('machine_ip', ''),
            'machine_key': kwargs.get('machine_key', ''),
            'machine_user': kwargs.get('machine_user', 'root'),
            'machine_port': kwargs.get('machine_port', 22)
        }
        return payload

    def _add_cloud_coreos(self, **kwargs):
        payload = {
            'machine_ip': kwargs.get('machine_ip', ''),
            'machine_key': kwargs.get('machine_key', ''),
            'machine_user': kwargs.get('machine_user', 'root'),
            'machine_port': kwargs.get('machine_port', 22)
        }
        return payload

    def _add_cloud_vcloud(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'organization': kwargs.get('organization', ''),
            'host': kwargs.get('host', ''),
            'indonesianRegion': kwargs.get('indonesianRegion', '')
        }
        return payload

    def _add_cloud_vsphere(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'host': kwargs.get('host', '')
        }
        return payload

    def _add_cloud_docker(self, **kwargs):
        payload = {
            'docker_port': int(kwargs.get('docker_port', 4243)),
            'docker_host': kwargs.get('docker_host', ''),
            'auth_user': kwargs.get('auth_user', ''),
            'auth_password': kwargs.get('auth_password', ''),
            'key_file': kwargs.get('key_file', ''),
            'cert_file': kwargs.get('cert_file', ''),
            'ca_cert_file': kwargs.get('ca_cert_file', '')
        }
        return payload

    def _add_cloud_libvirt(self, **kwargs):
        payload = {
            'machine_hostname': kwargs.get('machine_hostname', ''),
            'machine_user': kwargs.get('machine_user', 'root'),
            'machine_key': kwargs.get('machine_key', ''),
            'images_location': kwargs.get('images_location', ''),
            'ssh_port': kwargs.get('ssh_port', 22)
        }
        return payload

    # def _add_cloud_hp(self, **kwargs):
    #     payload = {
    #         'username': kwargs.get('username', ''),
    #         'password': kwargs.get('password', ''),
    #         'tenant_name': kwargs.get('tenant_name', ''),
    #         'region': kwargs.get('region', '')
    #     }
    #     return payload

    def _add_cloud_openstack(self, **kwargs):
        payload = {
            'username': kwargs.get('username', ''),
            'password': kwargs.get('password', ''),
            'auth_url': kwargs.get('auth_url', ''),
            'tenant_name': kwargs.get('tenant_name', ''),
            'region': kwargs.get('region', ''),
            'compute_endpoint': kwargs.get('compute_endpoint', '')
        }
        return payload

    def _add_cloud_hostvirtual(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_cloud_vultr(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', '')
        }
        return payload

    def _add_cloud_packet(self, **kwargs):
        payload = {
            'api_key': kwargs.get('api_key', ''),
            'project_id': kwargs.get('project_id', '')
        }
        return payload

    def _list_keys(self):
        """
        Retrieves a list of all added Keys and populates the self._keys dict with Key instances

        :returns: A list of Keys instances
        """
        req = self.request(self.uri + '/keys')
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
                    if (search in self._keys[key_id].id) or (search in self._keys[key_id].name)]
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

    def _generate_and_add_key(self, key_name):
        priv = self.generate_key()
        self.add_key(key_name, priv)

    def generate_key(self):
        """
        Ask mist.io to randomly generate a private ssh-key to be used with the creation of a new Key

        :returns: A string of a randomly generated ssh private key
        """
        req = self.request(self.uri + "/keys")
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
            'name': key_name,
            'priv': private
        }

        data = json.dumps(payload)

        req = self.request(self.uri + '/keys', data=data)
        response = req.put().json()

        self.update_keys()
        return response

    def _list_scripts(self):
        """
        """
        req = self.request(self.uri + '/scripts')
        scripts = req.get().json()
        if scripts:
            self._scripts = {}
            for script in scripts:
                self._scripts[script['script_id']] = Script(script, self)
        else:
            self._scripts = {}

    def scripts(self, id=None, search=None):
        """
        """
        if self._scripts is None:
            self._scripts = {}
            self._list_scripts()

        return [self._scripts[script_id] for script_id in self._scripts.keys()]

    def _list_machines(self):
        self._machines = []
        for cloud in self.clouds():
            machines = cloud.machines()
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

    def get_job(self, job_id):
        req = self.request(self.uri + '/jobs/' + job_id)
        response = req.get()
        return response.json()

    def end_job(self, job_id, exit_code=None, output=None, error=None,
                node_instances=[]):
        payload = {
            'exit_code': exit_code,
            'output': output,
            'error': error,
            'node_instances': node_instances
        }
        req = self.request(self.uri + "/jobs/" + job_id,
                           data=json.dumps(payload))
        response = req.delete()
        return response.json()

    # self.scripts() exists too
    def get_scripts(self, **_):
        req = self.request(self.uri + '/scripts')
        response = req.get()
        return response.json()

    # TODO: move these to Script?
    def add_script(self, **kwargs):
        payload = {
            'name': kwargs.get('name', ''),
            'description': kwargs.get('description', ''),
            'script': kwargs.get('script', ''),
            'location_type': kwargs.get('location_type', ''),
            'exec_type': kwargs.get('exec_type', ''),
            'entrypoint': kwargs.get('entrypoint')
        }

        req = self.request(self.uri + '/scripts',
                           data=json.dumps(payload), api_version=2)
        response = req.post()
        return response.json()

    def remove_script(self, script_id):
        req = self.request(self.uri + '/scripts/' + script_id,  api_version=2)
        response = req.delete()
        return response

    # exists in Machine model, too
    def run_script(self, cloud_id, machine_id, script_id, script_params="",
                   env=None, su=False, fire_and_forget=True):
        payload = {
            'cloud_id': cloud_id,
            'machine_id': machine_id,
            'params': script_params,
            'env': env,
            'su': su
        }

        data = json.dumps(payload)
        req = self.request(self.uri + "/scripts/" + script_id, data=data)
        re = req.post()
        re = re.json()
        if not fire_and_forget:
            job_id = re["job_id"]
            while True:
                job = self.client.get_job(job_id)
                if job["error"]:
                    raise Exception("Failed to run script")
                if job["finished_at"]:
                    break
                sleep(10)
        return re

    def add_and_run_script(self, cloud_id, machine_id, script_params="",
                           env=None, su=False, fire_and_forget=True, **kwargs):

        script = self.add_script(**kwargs)
        self.run_script(cloud_id, machine_id, script["script_id"],
                        script_params="", env=None, su=False,
                        fire_and_forget=True)

    def get_templates(self, **_):
        req = self.request(self.uri + '/templates')
        response = req.get()
        return response.json()

    def show_template(self, template_id):
        req = self.request(self.uri + '/templates/' + template_id)
        response = req.get()
        return response.json()

    def add_template(self, **kwargs):
        payload = {
            'name': kwargs.get('name', ''),
            'description': kwargs.get('description', ''),
            'template': kwargs.get('template', ''),
            'location_type': kwargs.get('location_type', ''),
            'exec_type': kwargs.get('exec_type', ''),
            'entrypoint': kwargs.get('entrypoint', ''),
        }

        req = self.request(self.uri + '/templates',
                           data=json.dumps(payload), api_version=2)
        response = req.post()
        return response.json()

    def delete_template(self, template_id):
        req = self.request(self.uri + '/templates/' + template_id)
        response = req.delete()
        return response

    def get_stacks(self):
        req = self.request(self.uri + '/stacks')
        response = req.get()
        return response.json()

    def create_stack(self, template_id, stack_name, stack_description, deploy,
                     inputs={}):
        payload = {
            'template_id': template_id,
            'inputs': inputs,
            'stack_name': stack_name,
            'stack_description': stack_description,
            'deploy': deploy
        }

        req = self.request(self.uri + "/stacks", data=json.dumps(payload))
        re = req.post()
        return re.json()

    def delete_stack(self, stack_id, inputs={}):
        payload = {
            'inputs': inputs
        }

        req = self.request(self.uri + "/stacks/" + stack_id,
                           data=json.dumps(payload))
        response = req.delete()
        return response

    def run_workflow(self, stack_id, workflow, inputs={}):
        payload = {
            'workflow': workflow,
            'inputs': inputs
        }

        req = self.request(self.uri + "/stacks/" + stack_id,
                           data=json.dumps(payload))
        response = req.post()
        return response.json()

    def show_stack(self, stack_id):

        req = self.request(self.uri + "/stacks/" + stack_id)
        response = req.get()
        return response.json()

    def list_tunnels(self):
        req = self.request(self.uri + '/tunnels')
        response = req.get()
        return response.json()

    def add_tunnel(self, name, cidrs, excluded_cidrs, description):
        payload = {
            'name': name,
            'cidrs': cidrs,
            'excluded_cidrs': excluded_cidrs,
            'description': description
        }
        
        req = self.request(self.uri + '/tunnels', data=json.dumps(payload))
        response = req.post()
        return response.json()

    def edit_tunnel(self, tunnel_id, name, cidrs, description):
        payload = {
            'name': name,
            'cidrs': cidrs,
            'description': description
        }

        req = self.request(self.uri + '/tunnel/' + tunnel_id,
                           data=json.dumps(payload))
        response = req.put()
        return response.json()

    def delete_tunnel(self, tunnel_id):
        req = self.request(self.uri + '/tunnel/' + tunnel_id)
        response = req.delete()
        return response

    def tunnel_script(self, tunnel_id):
        req = self.request(self.uri + '/tunnel/' + tunnel_id + '/script')
        response = req.get()
        return response.text

    def tunnel_command(self, tunnel_id):
        req = self.request(self.uri + '/tunnel/' + tunnel_id + '/command')
        response = req.get()
        return response.text
