import json
import os
import re

from time import time, sleep

from mistclient.helpers import RequestsHandler
from prettytable import PrettyTable


class Cloud(object):
    """
    A cloud instance.
    """
    def __init__(self, cloud, mist_client):
        """

        :param cloud: Dict that is returned from the API, with all the available info.
        :param mist_client: The MistClient instance that initiated the creation of this Cloud instance.
        :returns: A Cloud object.
        """
        self.mist_client = mist_client
        self.info = cloud
        self.title = cloud['title']
        self.id = cloud['id']
        self.enabled = cloud['enabled']
        self.provider = cloud['provider']
        self.api_token = self.mist_client.api_token

        self._machines = None

    def __str__(self):
        return "%s => %s, %s, %s" % (self.__class__.__name__, self.title, self.provider, self.id)

    def __repr__(self):
        return "%s => %s, %s, %s" % (self.__class__.__name__, self.title, self.provider, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token,
                               verify=self.mist_client.verify, **kwargs)

    def delete(self):
        """
        Delete the cloud from the list of added clouds in mist.io service.

        :returns: A list of mist.clients' updated clouds.
        """
        req = self.request(self.mist_client.uri + '/clouds/' + self.id)
        req.delete()
        self.mist_client.update_clouds()

    def rename(self, new_name):
        """
        Rename the cloud.

        :param new_name: New name for the cloud to be renamed to.
        :returns: A list of mist.clients' updated clouds.
        """
        payload = {
            'new_name': new_name
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + '/clouds/' + self.id, data=data)
        req.put()
        self.title = new_name
        self.mist_client.update_clouds()

    def enable(self):
        """
        Enable the Cloud.

        :returns:  A list of mist.clients' updated clouds.
        """
        payload = {
            "new_state": "1"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/clouds/'+self.id, data=data)
        req.post()
        self.enabled = True
        self.mist_client.update_clouds()

    def disable(self):
        """
        Disable the Cloud.

        :returns:  A list of mist.clients' updated clouds.
        """
        payload = {
            "new_state": "0"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/clouds/'+self.id, data=data)
        req.post()
        self.enabled = False
        self.mist_client.update_clouds()

    @property
    def sizes(self):
        """
        Available machine sizes to be used when creating a new machine.

        :returns: A list of available machine sizes.
        """
        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/sizes')
        sizes = req.get().json()
        return sizes

    @property
    def locations(self):
        """
        Available locations to be used when creating a new machine.

        :returns: A list of available locations.
        """
        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/locations')
        locations = req.get().json()
        return locations

    @property
    def networks(self):
        """
        Available networks.

        :returns: A list of available networks associated to a provider.
        """
        if self.provider in ['openstack', 'nephoscale']:
            req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/networks')
            networks = req.get().json()
            return networks
        else:
            print "Network actions not supported yet for %s provider" % self.provider

    def create_network(self, network, router=None, subnet=None):
        payload = {
          "network": network,
          "router": router,
          "subnet": subnet
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/networks',
                           data=data)
        return req.post().json()

    def delete_network(self, network):

        req = self.request(self.mist_client.uri + '/clouds/' + self.id + '/networks/' + network )
        req.delete()


    @property
    def images(self):
        """
        Available images to be used when creating a new machine.

        :returns: A list of all available images.
        """
        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/images')
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

        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/images', data=data)
        images = req.get().json()
        return images

    def _list_machines(self):
        """
        Request a list of all added machines.

        Populates self._machines dict with mist.client.model.Machine instances
        """
        try:
            req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/machines')
            machines = req.get().json()
        except:
            # Eg invalid cloud credentials
            machines = {}

        if machines:
            for machine in machines:
                self._machines[machine['id']] = Machine(machine, self)
        else:
            self._machines = {}

    def machines(self, id=None, name=None, search=None):
        """
        Property-like function to call the _list_machines function in order to populate self._machines dict

        :returns: A list of Machine instances.
        """
        if self._machines is None:
            self._machines = {}
            self._list_machines()

        if id:
            return [self._machines[machine_id] for machine_id in self._machines.keys()
                    if id == self._machines[machine_id].id]
        elif name:
            return [self._machines[machine_id] for machine_id in self._machines.keys()
                    if name == self._machines[machine_id].name]
        elif search:
            return [self._machines[machine_id] for machine_id in self._machines.keys()
                    if search in self._machines[machine_id].name
                    or search in self._machines[machine_id].id]
        else:
            return [self._machines[machine_id] for machine_id in self._machines.keys()]

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

    def create_machine(self, name, key, image_id, location_id, size_id,
                       image_extra="", disk="", script="", monitoring=False,
                       ips=[], networks=[], location_name="", async=False,
                       docker_command="", quantity=1, persist=False, fire_and_forget=True,
                       timeout=6000, script_id="", script_params="", verbose=False,
                       associate_floating_ip=False, provider=""):
        """
        Create a new machine on the given cloud

        :param name: Name of the machine
        :param key: Key Object to associate with the machine
        :param image_id: Id of image to be used with the creation
        :param location_id: Id of the cloud's location to create the machine
        :param size_id: If of the size of the machine
        :param image_extra: Needed only by Linode cloud
        :param disk: Needed only by Linode cloud
        :returns: An update list of added machines
        """
        if isinstance(key, basestring):
            key_id = key
        else:
            key_id = key.id

        payload = {
            'name': name,
            'provider': provider,
            'key': key_id,
            'image': image_id,
            'location': location_id,
            'size': size_id,
            'image_extra': image_extra,
            'disk': disk,
            'script': script,
            'monitoring': monitoring,
            'ips': ips,
            'networks': networks,
            'location_name': location_name,
            'docker_command': docker_command,
            'async': async,
            'quantity': quantity,
            'persist': persist,
            'associate_floating_ip': associate_floating_ip
        }
        # add as params only if they are provided
        if script_id:
            payload['script_id'] = script_id
        if script_params:
            payload['script_params'] = script_params
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/clouds/'+self.id+'/machines', data=data)
        result = req.post()
        self.update_machines()

        if not async or fire_and_forget:
            return result
        else:
            job_id = result.json()['job_id']

            started_at = time()
            while True:
                job = self.mist_client.get_job(job_id)

                if verbose:
                    summary = job.get('summary', {})

                    probes = summary.get('probe', {})
                    creates = summary.get('create', {})
                    scripts = summary.get('script', {})
                    monitoring = summary.get('monitoring', {})

                    states = [
                        'success',
                        'error',
                        'skipped',
                        'pending'
                    ]

                    x = PrettyTable(['', 'SUCCESS', 'ERROR', 'SKIPPED', 'PENDING'])

                    if creates:
                        machines_created = {}
                        for state in states:
                            machines_created[state] = '%s/%s' % (creates.get(state, 'Undefined'), quantity)
                        x.add_row(["Create:", machines_created['success'], machines_created['error'],
                                   machines_created['skipped'], machines_created['pending']])

                    if probes:
                        probed_machines = {}
                        for state in states:
                            probed_machines[state] = '%s/%s' % (probes.get(state, 'Undefined'), quantity)
                        x.add_row(["Probe:", probed_machines['success'], probed_machines['error'],
                                   probed_machines['skipped'], probed_machines['pending']])

                    if scripts:
                        scripted_machines = {}
                        for state in states:
                            scripted_machines[state] = '%s/%s' % (scripts.get(state, 'Undefined'), quantity)
                        x.add_row(["Script:", scripted_machines['success'], scripted_machines['error'],
                                   scripted_machines['skipped'], scripted_machines['pending']])

                    if monitoring:
                        monitored_machines = {}
                        for state in states:
                            monitored_machines[state] = '%s/%s' % (monitoring.get(state, 'Undefined'), quantity)
                        x.add_row(["Monitoring:", monitored_machines['success'], monitored_machines['error'],
                                   monitored_machines['skipped'], monitored_machines['pending']])

                    print x
                    print

                if job.get('finished_at', 0):
                    error = job.get('error', None)
                    if verbose and error:
                        print "Finished with errors:"
                        logs = job.get('logs', [])
                        for log in logs:
                            error = log.get('error', None)
                            if error:
                                print " - ", error
                        raise Exception("Create machine failed. Check the logs.")
                    elif verbose and not error:
                        print "Finished without errors!"
                    self.update_machines()
                    return job

                elif time() - started_at > timeout:
                    print "Timed out!"
                    raise Exception("Create machine timed out. Check the logs.")
                    return job

                sleep(5)


class Machine(object):
    """
    A machine instance
    """
    def __init__(self, machine, cloud):
        """

        :param machine: Dict with all available info for the machine
        :param cloud: The Cloud instance which initiates the new machine
        :returns: A machine instance
        """
        self.cloud = cloud
        self.mist_client = cloud.mist_client
        self.info = machine
        self.api_token = self.mist_client.api_token
        self.name = machine['name']
        self.id = machine['id']
        self.probed = None

    def __str__(self):
        return "%s => %s, %s" % (self.__class__.__name__, self.name, self.id)

    def __repr__(self):
        return "%s => %s, %s" % (self.__class__.__name__, self.name, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    # exists in MistClient, too
    # def run_script(self, script_id, params="", su=False, fire_and_forget=True):
    #     script_job = self.mist_client.run_script(script_id=script_id, cloud_id=self.cloud.id,
    #                                machine_id=self.id,
    #                                script_params=script_params,
    #                                su=su)
    #
    #     return script_job

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
        req = self.request(self.mist_client.uri+'/clouds/'+self.cloud.id+'/machines/'+self.id, data=data)
        req.post()
        self.cloud.update_machines()

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
        If no parameter is provided, mist.io will try to probe the machine with
        the default
        :param key_id: Optional. Give if you explicitly want to probe with this
        key_id
        :param ssh_user: Optional. Give if you explicitly want a specific user
        :returns: A list of data received by the probing (e.g. uptime etc)
        """
        ips = [ip for ip in self.info['public_ips'] if ':' not in ip]

        if not ips:
            raise Exception("No public IPv4 address available to connect to")
        payload = {
            'host': ips[0],
            'key': key_id,
            'ssh_user': ssh_user
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + "/clouds/" + self.cloud.id +
                           "/machines/" + self.id + "/probe", data=data)
        probe_info = req.post().json()
        self.probed = True
        return probe_info

    # def associate_key(self, key_id, host=None, ssh_user=None, ssh_port=22):
    #     payload = {
    #         'ssh_user': ssh_user,
    #         'host': host,
    #         'ssh_port': ssh_port
    #     }
    #     data = json.dumps(payload)
    #     req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/keys/"+key_id,
    #                        data=data)
    #     req.put()
    #     self.mist_client.update_keys()

    def _toggle_monitoring(self, action, no_ssh=False):
        """
        Enable or disable monitoring on a machine

        :param action: Can be either "enable" or "disable"
        """
        payload = {
            'action': action,
            'name': self.name,
            'no_ssh': no_ssh,
            'public_ips': self.info['public_ips'],
            'dns_name': self.info['extra'].get('dns_name', 'n/a')
        }

        data = json.dumps(payload)

        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/monitoring",
                           data=data)
        req.post()

    def enable_monitoring(self, no_ssh=False):
        """
        Enable monitoring
        """
        return self._toggle_monitoring(action="enable", no_ssh=no_ssh)

    def disable_monitoring(self, no_ssh=False):
        """
        Disable monitoring
        """
        return self._toggle_monitoring(action="disable", no_ssh=no_ssh)

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
        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/stats", data=data)
        stats = req.get().json()
        return stats

    @property
    def available_metrics(self):
        """
        List all available metrics that you can add to this machine

        :returns: A list of dicts, each of which is a metric that you can add to a monitored machine
        """
        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/metrics")
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
        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/metrics", data=data)
        req.put()

    def remove_metric(self, metric_id):
        """
        Remove a metric from a monitored machine

        :param metric_id: Metric_id (provided by self.get_stats() )
        """
        payload = {
            'metric_id': metric_id
        }

        data = json.dumps(payload)

        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/metrics", data=data)
        req.delete()

    def add_python_plugin(self, name, python_file, value_type="gauge", unit=None):
        """
        Add a custom python plugin to the collectd instance of a monitored plugin

        :param python_file: Path of the python file to be added as custom python plugin
        :param name: Name of the plugin
        :param value_type: Optional. Can be either "gauge" or "derive"
        :param unit: Optional. If given the new plugin will be measured according to this unit
        """

        if not os.path.isfile(python_file):
            raise Exception(python_file, "is not a file or could not be found in tho given path")

        with open(python_file) as f:
            script = f.read()

        payload = {
            'plugin_type': 'python',
            'name': name,
            'unit': unit,
            'value_type': value_type,
            'read_function': script,
            'host': self.info['public_ips'][0]
        }

        data = json.dumps(payload)

        #PLugin id must be in lowercase
        plugin_id = name.lower()

        #PLugin id must contain only alphanumeric chars
        pattern = re.compile('\W')
        plugin_id = re.sub(pattern, "_", plugin_id)

        #Plugin id should not have double underscores
        while "__" in plugin_id:
            pattern = "\r?__"
            plugin_id = re.sub(pattern, "_", plugin_id)

        #Plugin id should not have underscore as first or last char
        if plugin_id[-1] == "_":
            plugin_id = plugin_id[:-2]

        if plugin_id[0] == "_":
            plugin_id = plugin_id[1:]

        req = self.request(self.mist_client.uri+"/clouds/"+self.cloud.id+"/machines/"+self.id+"/plugins/"+plugin_id,
                           data=data)
        req.post()

    def add_tag(self, key, value):
        # TODO: multiple tags
        payload = {
          'tags': {
              key: value
          }
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + "/clouds/" + self.cloud.id +
                           "/machines/" + self.id + "/tags", data=data)
        req.post()
        self.cloud.update_machines()

    def del_tag(self, key, value):
        # TODO: multiple tags
        payload = {
            'value': value
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + "/clouds/" + self.cloud.id +
                           "/machines/" + self.id + "/tags/" + key, data=data)
        req.delete()
        self.cloud.update_machines()


class Key(object):
    """
    A Key instance
    """
    def __init__(self, key, mist_client):
        """

        :param key: A dict with all the available info for this key
        :param mist_client: The MistClient instance that initiated the creation of this Key instance.
        :returns: A Key instance
        """
        self.mist_client = mist_client
        self.api_token = self.mist_client.api_token
        self.id = key['id']
        self.name = key['name']
        self.is_default = key['isDefault']
        self.name = key["name"]
        self.info = key

    def __str__(self):
        return "%s => %s" % (self.__class__.__name__, self.name)

    def __repr__(self):
        return "%s => %s" % (self.__class__.__name__, self.name)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the
        api_token and all the other params to the requests that are being made

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
            'new_name': new_name
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

    def associate(self, cloud_id, machine_id, host=None,
                  ssh_user=None, ssh_port=22):
        payload = {
            'ssh_user': ssh_user,
            'host': host,
            'ssh_port': ssh_port
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + "/clouds/" + cloud_id +
                           "/machines/" + machine_id + "/keys/" + self.id,
                           data=data)
        req.put()
        self.mist_client.update_keys()

    def disassociate(self, cloud_id, machine_id, host=None):
        payload = {
            'host': host
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + "/clouds/" + cloud_id +
                           "/machines/" + machine_id + "/keys/" + self.id,
                           data=data)
        req.delete()
        self.mist_client.update_keys()


class Script(object):
    """
    A script instance
    """
    def __init__(self, script, mist_client):
        """

        """
        self.mist_client = mist_client
        self.api_token = self.mist_client.api_token
        self.id = script['script_id']
        self.name = script['name']
        self.description = script['description']

    def __str__(self):
        return "%s => %s" % (self.__class__.__name__, self.name)

    def __repr__(self):
        return "%s => %s" % (self.__class__.__name__, self.name)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)


# # TODO
# class Template(object):
#     """
#     A Template instance
#     """
#     def __init__(self, template, mist_client):
#
#
# class Stack(object):
#     """
#     A Stack instance
#     """
#     def __init__(self, stack, mist_client):
