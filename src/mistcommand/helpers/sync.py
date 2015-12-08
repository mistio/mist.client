import os
import sys
import getpass

from yaml import load
from yaml.scanner import ScannerError

from mistclient import MistClient
from mistclient.helpers import machine_from_id, cloud_from_id


def load_dbyaml(path):
    if not os.path.isfile(path):
        print "You need to provide a valid path for a db.yaml file"
        sys.exit(1)

    with open(path, 'r') as db_yaml:
        try:
            print ">>>Loading %s" %path
            print
            user_dict = load(db_yaml) or {}
            return user_dict
        except ScannerError:
            print "Error parsing %s" % path
            print "Maybe not a yaml file"
            sys.exit(1)


def init_client():
    print ">>>Log in to mist.io"
    email = raw_input("Email: ")
    password = getpass.getpass("Password: ")
    print
    try:
        client = MistClient(email=email, password=password)
        client.clouds
        return client
    except Exception as e:
        print e
        sys.exit(1)


def add_cloud(client, cloud):
    title = cloud.get('title')
    provider = cloud.get('provider')
    key = cloud.get('apikey', "")
    secret = cloud.get('apisecret', "")
    tenant_name = cloud.get('tenant_name', "")
    region = cloud.get('region', "")
    apiurl = cloud.get('apiurl', "")
    compute_endpoint = cloud.get('compute_endpoint', None)
    machine_ip = cloud.get('machine_ip', None)
    machine_key = cloud.get('machine_key', None)
    machine_user = cloud.get('machine_user', None)
    machine_port = cloud.get('machine_port', None)
    client.add_cloud(title, provider, key, secret, tenant_name=tenant_name, region=region, apiurl=apiurl,
                       machine_ip=machine_ip, machine_key=machine_key, machine_user=machine_user,
                       compute_endpoint=compute_endpoint, machine_port=machine_port)


def add_bare_metal_cloud(client, cloud, keys):
    """
    Black magic is happening here. All of this wil change when we sanitize our API, however, this works until then
    """
    title = cloud.get('title')
    provider = cloud.get('provider')
    key = cloud.get('apikey', "")
    secret = cloud.get('apisecret', "")
    tenant_name = cloud.get('tenant_name', "")
    region = cloud.get('region', "")
    apiurl = cloud.get('apiurl', "")
    compute_endpoint = cloud.get('compute_endpoint', None)
    machine_ip = cloud.get('machine_ip', None)
    machine_key = cloud.get('machine_key', None)
    machine_user = cloud.get('machine_user', None)
    machine_port = cloud.get('machine_port', None)

    if provider == "bare_metal":
        machine_ids = cloud['machines'].keys()
        bare_machine = cloud['machines'][machine_ids[0]]
        machine_hostname = bare_machine.get('dns_name', None)
        if not machine_hostname:
            machine_hostname = bare_machine['public_ips'][0]

        if not machine_ip:
            machine_ip = machine_hostname
        key = machine_hostname
        machine_name = cloud['machines'][machine_ids[0]]['name']
        machine_id = machine_ids[0]

        keypairs = keys.keys()
        for i in keypairs:
            keypair_machines = keys[i]['machines']
            if keypair_machines:
                keypair_machs = keys[i]['machines']
                for mach in keypair_machs:
                    if mach[1] == machine_id:
                        machine_key = i
                        break
            else:
                pass

    client.add_cloud(title, provider, key, secret, tenant_name=tenant_name, region=region, apiurl=apiurl,
                       machine_ip=machine_ip, machine_key=machine_key, machine_user=machine_user,
                       compute_endpoint=compute_endpoint, machine_port=machine_port)


def sync_clouds(user_dict, client):
    added_clouds = user_dict['clouds']
    clouds = client.clouds

    print ">>>Syncing clouds"
    for key in added_clouds:
        if key in clouds.keys():
            print "Found %s" % added_clouds[key]['title']
        else:
            print "Adding cloud %s" % added_clouds[key]['title']
            if added_clouds[key]['provider'] == "bare_metal":
                add_bare_metal_cloud(client, added_clouds[key], user_dict['keypairs'])
            else:
                add_cloud(client, added_clouds[key])
    print


def add_key(client, key, key_id):
    key_name = key_id
    private = key['private']
    client.add_key(key_name=key_name, private=private)

    if key['default']:
        client.update_keys()
        chosen_key = client.keys[key_id]
        chosen_key.set_default()


def sync_keys(user_dict, client):
    added_keys = user_dict['keypairs']
    keys = client.keys

    print ">>>Syncing keys"
    for key in added_keys:
        if key in keys.keys():
            print "Found %s" % key
        else:
            print "Adding key %s" % key
            add_key(client, key=added_keys[key], key_id=key)
    print


def associate_keys(user_dict, client):
    """
    This whole function is black magic, had to however cause of the way we keep key-machine association
    """
    added_keys = user_dict['keypairs']

    print ">>>Updating Keys-Machines association"
    for key in added_keys:
        machines = added_keys[key]['machines']
        if machines:
            try:
                for machine in machines:
                    cloud_id = machine[0]
                    machine_id = machine[1]
                    ssh_user = machine[3]
                    ssh_port = machine[-1]
                    key = client.keys[key]
                    cloud = cloud_from_id(client, cloud_id)
                    cloud.update_machines()
                    mach = machine_from_id(cloud, machine_id)
                    public_ips = mach.info.get('public_ips', None)
                    if public_ips:
                        host = public_ips[0]
                    else:
                        host = ""
                    key.associate_to_machine(cloud_id=cloud_id, machine_id=machine_id, host=host, ssh_port=ssh_port,
                                             ssh_user=ssh_user)

                    print "associated machine %s" % machine_id
            except Exception as e:
                pass
    client.update_keys()
    print


def sync(path):

    user_dict = load_dbyaml(path)
    client = init_client()
    sync_keys(user_dict, client)
    sync_clouds(user_dict, client)
    associate_keys(user_dict, client)