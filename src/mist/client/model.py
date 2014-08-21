import json

from time import time

from mist.client.helpers import RequestsHandler


class Backend(object):
    """
    A backend instance.
    """
    def __init__(self, backend, mist_client):
        """

        :param backend: Dict that is returned from the API, with all the available info.
        :param mist_client: The MistClient instance that initiated the creation of this Backend instance.
        :returns: A Backend object.
        """
        self.mist_client = mist_client
        self.info = backend
        self.title = backend['title']
        self.id = backend['id']
        self.enabled = backend['enabled']
        self.provider = backend['provider']
        self.api_token = self.mist_client.api_token

        self._machines = None

    def __str__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.title, self.id)

    def __repr__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.title, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    def delete(self):
        """
        Delete the backend from the list of added backends in mist.io service.

        :returns: A list of mist.clients' updated backends.
        """
        req = self.request(self.mist_client.uri + '/backends/' + self.id)
        req.delete()
        self.mist_client.update_backends()

    def rename(self, new_name):
        """
        Rename the backend.

        :param new_name: New name for the backend to be renamed to.
        :returns: A list of mist.clients' updated backends.
        """
        payload = {
            'new_name': new_name
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + '/backends/' + self.id, data=data)
        req.put()
        self.title = new_name
        self.mist_client.update_backends()

    def enable(self):
        """
        Enable the Backend.

        :returns:  A list of mist.clients' updated backends.
        """
        payload = {
            "new_state": "1"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.id, data=data)
        req.post()
        self.enabled = True
        self.mist_client.update_backends()

    def disable(self):
        """
        Disable the Backend.

        :returns:  A list of mist.clients' updated backends.
        """
        payload = {
            "new_state": "0"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.id, data=data)
        req.post()
        self.enabled = False
        self.mist_client.update_backends()

    @property
    def sizes(self):
        """
        Available machine sizes to be used when creating a new machine.

        :returns: A list of available machine sizes.
        """
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/sizes')
        sizes = req.get().json()
        return sizes

    @property
    def locations(self):
        """
        Available locations to be used when creating a new machine.

        :returns: A list of available locations.
        """
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/locations')
        locations = req.get().json()
        return locations

    @property
    def images(self):
        """
        Available images to be used when creating a new machine.

        :returns: A list of all available images.
        """
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/images')
        images = req.get().json()
        return images

    def search_image(self, search_term):
        """
        Search for a specific image by providing a search term (mainly used with ec2's community and public images)

        :param search_term: Search term to be used when searching for images's names containing this term.
        :returns: A list of all images, whose names contain the given search_term.
        """
        payload = {
            'search_term': search_term
        }
        data = json.dumps(payload)

        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/images', data=data)
        images = req.get().json()
        return images

    def _list_machines(self):
        """
        Request a list of all added machines.

        Populates self._machines dict with mist.client.model.Machine instances
        """
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/machines')
        machines = req.get().json()

        if machines:
            for machine in machines:
                self._machines[machine['name']] = Machine(machine, self)
        else:
            self._machines = {}

    @property
    def machines(self):
        """
        Property-like function to call the _list_machines function in order to populate self._machines dict

        :returns: A list of Machine instances.
        """
        if self._machines is None:
            self._machines = {}
            self._list_machines()

        return self._machines

    def update_machines(self):
        """
        Update added machines' info and re-populate the self._machines dict.

        This one is used whenever a new machine is created, rebooted etc etc or whenever you want to update the list
        of added machines.

        :returns: A list of Machine instances.
        """
        self._machines = {}
        self._list_machines()
        return self._machines

    def create_machine(self, name, key, image_id, location_id, size_id, image_extra="", disk=""):
        """
        Create a new machine on the given backend

        :param name: Name of the machine
        :param key: Key Object to associate with the machine
        :param image_id: Id of image to be used with the creation
        :param location_id: Id of the backend's location to create the machine
        :param size_id: If of the size of the machine
        :param image_extra: Needed only by Linode backend
        :param disk: Needed only by Linode backend
        :returns: An update list of added machines
        """
        payload = {
            'name': name,
            'key': key.id,
            'image': image_id,
            'location': location_id,
            'size': size_id,
            'image_extra': image_extra,
            'disk': disk
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/machines', data=data)
        req.post()
        self.update_machines()


class Machine(object):
    """
    A machine instance
    """
    def __init__(self, machine, backend):
        """

        :param machine: Dict with all available info for the machine
        :param backend: The Backend instance which initiates the new machine
        :returns: A machine instance
        """
        self.backend = backend
        self.mist_client = backend.mist_client
        self.info = machine
        self.api_token = self.mist_client.api_token
        self.name = machine['name']
        self.id = machine['id']
        self.probed = None

    def __str__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.name, self.id)

    def __repr__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.name, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    def _machine_actions(self, action):
        """
        Actions for the machine (e.g. stop, start etc)

        :param action: Can be "reboot", "start", "stop", "destroy"
        :returns: An updated list of the added machines
        """
        payload = {
            'action': action
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.backend.id+'/machines/'+self.id, data=data)
        req.post()
        self.backend.update_machines()

    def reboot(self):
        """
        Reboot machine
        """
        self._machine_actions("reboot")

    def start(self):
        """
        Start a stopped machine
        """
        self._machine_actions("start")

    def stop(self):
        """
        Stop a running machine
        """
        self._machine_actions("stop")

    def destroy(self):
        """
        Destroy machine
        """
        self._machine_actions("destroy")

    def probe(self, key_id=None, ssh_user=None):
        """
        If no parameter is provided, mist.io will try to probe the machine with the default
        :param key_id: Optional. Give if you explicitly want to probe with this key_id
        :param ssh_user: Optional. Give if you explicitly want a specific user
        :returns: A list of data received by the probing (e.g. uptime etc)
        """
        payload = {
            'host': self.info['public_ips'][0],
            'key': key_id,
            'ssh_user': ssh_user
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+"/backends/"+self.backend.id+"/machines/"+self.id+"/probe", data=data)
        probe_info = req.post().json()
        self.probed = True
        return probe_info

    def _toggle_monitoring(self, action):
        """
        Enable or disable monitoring on a machine

        :param action: Can be either "enable" or "disable"
        """
        payload = {
            'action': action,
            'machine_name': self.name,
            'public_ips': self.info['public_ips'],
            'dns_name': self.info['extra'].get('dns_name', 'n/a')
        }

        data = json.dumps(payload)

        req = self.request(self.mist_client.uri+"/backends/"+self.backend.id+"/machines/"+self.id+"/monitoring",
                           data=data)
        req.post()

    def enable_monitoring(self):
        """
        Enable monitoring
        """
        self._toggle_monitoring(action="enable")

    def disable_monitoring(self):
        """
        Disable monitoring
        """
        self._toggle_monitoring(action="disable")

    def get_stats(self, start=int(time()), stop=int(time())+10, step=10):
        """
        Get stats of a monitored machine

        :param start: Time formatted as integer, from when to fetch stats (default now)
        :param stop: Time formatted as integer, until when to fetch stats (default +10 seconds)
        :param step: Step to fetch stats (default 10 seconds)
        :returns: A dict of stats
        """
        payload = {
            'v': 2,
            'start': start,
            'stop': stop,
            'step': step
        }

        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+"/backends/"+self.backend.id+"/machines/"+self.id+"/stats", data=data)
        stats = req.get().json()
        return stats

    @property
    def available_metrics(self):
        """
        List all available metrics that you can add to this machine

        :returns: A list of dicts, each of which is a metric that you can add to a monitored machine
        """
        req = self.request(self.mist_client.uri+"/backends/"+self.backend.id+"/machines/"+self.id+"/metrics")
        metrics = req.get().json()
        return metrics

    def add_metric(self, metric_id):
        """
        Add a metric to a monitored machine

        :param metric_id: Metric_id (provided by self.available_metrics)
        """
        payload = {
            'metric_id': metric_id
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+"/backends/"+self.backend.id+"/machines/"+self.id+"/metrics", data=data)
        req.put()


class Key(object):
    """
    A Key instance
    """
    def __init__(self, key, mist_client):
        """

        :param key: A dict with all the available info for this key
        :param mist_client: The MistClient instance that initiated the creation of this Key instance.
        :return:
        """
        self.mist_client = mist_client
        self.api_token = self.mist_client.api_token
        self.id = key['id']
        self.is_default = key['isDefault']
        self.info = key

    def __str__(self):
        return "%s => %s" % (self.__class__.__name__, self.id)

    def __repr__(self):
        return "%s => %s" % (self.__class__.__name__, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    @property
    def private(self):
        """
        Return the private ssh-key

        :returns: The private ssh-key as string
        """
        req = self.request(self.mist_client.uri+'/keys/'+self.id+"/private")
        private = req.get().json()
        return private

    @property
    def public(self):
        """
        Return the public ssh-key

        :returns: The public ssh-key as string
        """
        req = self.request(self.mist_client.uri+'/keys/'+self.id+"/public")
        public = req.get().json()
        return public

    def rename(self, new_name):
        """
        Rename a key

        :param new_name: New name for the key (will also serve as the key's id)
        :returns: An updated list of added keys
        """
        payload = {
            'new_id': new_name
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/keys/'+self.id, data=data)
        req.put()
        self.id = new_name
        self.mist_client.update_keys()

    def set_default(self):
        """
        Set this key as the default key

        :returns: An updated list of added keys
        """
        req = self.request(self.mist_client.uri+'/keys/'+self.id)
        req.post()
        self.is_default = True
        self.mist_client.update_keys()

    def delete(self):
        """
        Delete this key from mist.io

        :returns: An updated list of added keys
        """
        req = self.request(self.mist_client.uri+'/keys/'+self.id)
        req.delete()
        self.mist_client.update_keys()