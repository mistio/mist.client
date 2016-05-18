import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def show_cloud(cloud):
    x = PrettyTable(["Title", "ID", "Provider", "State"])
    x.add_row([cloud.title, cloud.id, cloud.provider, cloud.info['state']])
    print x
    print

    print "Machines:"
    x = PrettyTable(["Name", "ID", "State", "Public Ips"])
    machines = cloud.machines()

    for machine in machines:
        try:
            public_ips = machine.info['public_ips']
            ips = " -- ".join(public_ips)
        except:
            ips = ""
        x.add_row([machine.name, machine.id, machine.info['state'], ips])

    print x


def list_clouds(client, pretty):
    clouds = client.clouds()
    if not client.clouds():
        print "No clouds found"
        sys.exit(0)

    if pretty:
        x = PrettyTable(["Name", "ID", "Provider", "State"])
        for cloud in clouds:
            x.add_row([cloud.title, cloud.id, cloud.provider, cloud.info['state']])

        print x
    else:
        for cloud in clouds:
            # print cloud.title, cloud.id, cloud.provider, cloud.info['state']
            print "%-40s %-40s %-30s %-20s" % (cloud.title, cloud.id, cloud.provider, cloud.info['state'])


def choose_cloud(client, args):
    cloud_id = args.id
    cloud_name = args.name
    if cloud_id:
        clouds = client.clouds(id=cloud_id) or None
        cloud = clouds[0] if clouds else None
    elif cloud_name:
        clouds = client.clouds(name=cloud_name)
        cloud = clouds[0] if clouds else None
    else:
        clouds = client.clouds(search=args.cloud)
        cloud = clouds[0] if clouds else None

    return cloud


def return_cloud(client, args):
    cloud_id = args.cloud_id
    cloud_name = args.cloud_name
    if cloud_id:
        clouds = client.clouds(id=cloud_id) or None
        cloud = clouds[0] if clouds else None
    elif cloud_name:
        clouds = client.clouds(name=cloud_name)
        cloud = clouds[0] if clouds else None
    else:
        clouds = client.clouds(search=args.cloud)
        cloud = clouds[0] if clouds else None

    return cloud


def add_cloud(client, args):
    provider = args.provider
    if "ec2" in provider:
        add_ec2_cloud(client, args)
    elif "rackspace" in provider:
        add_rackspace_cloud(client, args)
    elif "nepho" in provider:
        add_nepho_cloud(client, args)
    elif "digi" in provider:
        add_digital_cloud(client,args)
    elif "linode" in provider:
        add_linode_cloud(client, args)
    elif "openstack" in provider:
        add_openstack_cloud(client, args)
    elif "softlayer" in provider:
        add_softlayer_cloud(client, args)
    # elif "hp" in provider:
    #     add_hp_cloud(client, args)
    elif "docker" in provider:
        add_docker_cloud(client, args)
    elif "azure" in provider:
        add_azure_cloud(client, args)
    elif "bare" in provider:
        add_bare_metal_cloud(client, args)
    elif provider == "coreos":
        add_coreos_cloud(client, args)
    elif "gce" in provider:
        add_gce_cloud(client, args)
    elif provider == "vcloud":
        add_vcloud_cloud(client, args)
    elif provider == "indonesian_vcloud":
        add_indonesian_cloud(client, args)
    elif provider == 'vsphere':
        add_vsphere_cloud(client, args)
    elif provider == "libvirt":
        add_libvirt_cloud(client, args)
    elif provider == 'hostvirtual':
        add_hostvirtual_cloud(client, args)
    elif provider == 'vultr':
        add_vultr_cloud(client, args)
    elif provider == 'packet':
        add_packet_cloud(client, args)


def add_gce_cloud(client, args):
    title = args.name
    provider = args.provider

    email = args.gce_email
    project_id = args.gce_project_id
    private_key_path = args.gce_private_key

    if private_key_path:
        with open(private_key_path, 'r') as f:
            private_key = f.read()
    else:
        private_key = ""

    client.add_cloud(title=title, provider=provider, email=email, project_id=project_id,
                       private_key=private_key)


def add_libvirt_cloud(client, args):
    title = args.name
    provider = args.provider
    machine_hostname = args.libvirt_hostname
    machine_user = args.libvirt_user
    machine_key = args.libvirt_key
    images_location = args.libvirt_images
    ssh_port = args.libvirt_ssh_port

    client.add_cloud(title=title, provider=provider,
                     machine_hostname=machine_hostname,
                     machine_user=machine_user, machine_key=machine_key,
                     images_location=images_location, ssh_port=ssh_port)


def add_vcloud_cloud(client, args):
    title = args.name
    provider = args.provider

    username = args.vcloud_username
    password = args.vcloud_password
    organization = args.vcloud_organization
    host = args.vcloud_host

    client.add_cloud(title=title, provider=provider, username=username, password=password,
                       organization=organization, host=host)

def add_vsphere_cloud(client, args):
    title = args.name
    provider = args.provider
    username = args.vsphere_username
    password = args.vsphere_password
    host = args.vsphere_host

    client.add_cloud(title=title, provider=provider, username=username,
                     password=password, host=host)


def add_indonesian_cloud(client, args):
    title = args.name
    provider = args.provider
    username = args.indonesian_username
    password = args.indonesian_password
    organization = args.indonesian_organization
    indonesianRegion = args.indonesian_region

    client.add_cloud(title=title, provider=provider, username=username,
                     password=password, organization=organization,
                     indonesianRegion=indonesianRegion)


def add_docker_cloud(client, args):
    title = args.name
    provider = args.provider
    docker_host = args.docker_host
    docker_port = args.docker_port
    docker_auth_user = args.docker_auth_user
    docker_auth_password = args.docker_auth_password
    if args.docker_key_file:
        with open(args.docker_key_file, 'r') as f:
            key_file = f.read()
    else:
        key_file = ""
    if args.docker_cert_file:
        with open(args.docker_cert_file, 'r') as f:
            cert_file = f.read()
    else:
        cert_file = ""
    if args.docker_ca_cert_file:
        with open(args.docker_ca_cert_file, 'r') as f:
            ca_cert_file = f.read()
    else:
        ca_cert_file = ""

    client.add_cloud(title=title, provider=provider, docker_host=docker_host,
                     docker_port=docker_port, auth_user=docker_auth_user,
                     auth_password=docker_auth_password, key_file=key_file,
                     cert_file=cert_file, ca_cert_file=ca_cert_file)


def add_azure_cloud(client, args):
    title = args.name
    provider = args.provider

    subscription_id = args.azure_sub_id
    with open(args.azure_cert_path) as f:
        certificate = f.read()

    client.add_cloud(title=title, provider=provider, subscription_id=subscription_id, certificate=certificate)


def add_ec2_cloud(client, args):
    title = args.name
    provider = args.provider

    api_key = args.ec2_api_key
    api_secret = args.ec2_api_secret
    region = args.ec2_region

    client.add_cloud(title=title, provider=provider, api_key=api_key, api_secret=api_secret, region=region)


def add_rackspace_cloud(client, args):
    title = args.name
    provider = args.provider

    username = args.rackspace_username
    api_key = args.rackspace_api_key
    region = args.rackspace_region

    client.add_cloud(title=title, provider=provider, username=username, api_key=api_key, region=region)


def add_nepho_cloud(client, args):
    title = args.name
    provider = args.provider

    username = args.nepho_username
    password = args.nepho_password

    client.add_cloud(title=title, provider=provider, username=username, password=password)


def add_digital_cloud(client, args):
    title = args.name
    provider = args.provider

    token = args.digi_token

    client.add_cloud(title=title, provider=provider, token=token)


def add_linode_cloud(client, args):
    title = args.name
    provider = args.provider

    api_key = args.linode_api_key

    client.add_cloud(title=title, provider=provider, api_key=api_key)


def add_openstack_cloud(client, args):
    title = args.name
    provider = args.provider

    username = args.openstack_username
    password = args.openstack_password
    auth_url = args.openstack_auth_url
    tenant_name = args.openstack_tenant
    region = args.openstack_region

    client.add_cloud(title=title, provider=provider, username=username, password=password,
                       auth_url=auth_url, tenant_name=tenant_name, region=region)


def add_softlayer_cloud(client, args):
    title = args.name
    provider = args.provider

    username = args.softlayer_username
    api_key = args.softlayer_api_key

    client.add_cloud(title=title, provider=provider, username=username, api_key=api_key)


# def add_hp_cloud(client, args):
#     title = args.name
#     provider = args.provider
#     username = args.hp_username
#     password = args.hp_password
#     tenant_name = args.hp_tenant
#     region = args.hp_region
#
#     client.add_cloud(title=title, provider=provider, username=username,
#                      password=password, tenant_name=tenant_name, region=region)


def add_bare_metal_cloud(client, args):
    title = args.name
    provider = args.provider
    machine_ip = args.bare_hostname
    machine_user = args.bare_user
    machine_port = args.bare_port
    machine_key = args.bare_ssh_key_id

    client.add_cloud(title=title, provider=provider, machine_ip=machine_ip,
                     machine_key=machine_key, machine_port=machine_port,
                     machine_user=machine_user)


def add_coreos_cloud(client, args):
    title = args.name
    provider = args.provider
    machine_ip = args.core_hostname
    machine_user = args.core_user
    machine_port = args.core_port
    machine_key = args.core_ssh_key_id

    client.add_cloud(title=title, provider=provider, machine_ip=machine_ip,
                     machine_key=machine_key, machine_port=machine_port,
                     machine_user=machine_user)


def add_hostvirtual_cloud(client, args):
    title = args.name
    provider = args.provider
    api_key = args.hostvirtual_api_key

    client.add_cloud(title=title, provider=provider, api_key=api_key)


def add_vultr_cloud(client, args):
    title = args.name
    provider = args.provider
    api_key = args.vultr_api_key

    client.add_cloud(title=title, provider=provider, api_key=api_key)


def add_packet_cloud(client, args):
    title = args.name
    provider = args.provider
    api_key = args.packet_api_key
    project_id = args.packet_project

    client.add_cloud(title=title, provider=provider, api_key=api_key,
                     project_id=project_id)


def cloud_action(args):

    client = authenticate()

    if args.action == 'list-clouds':
        pretty = args.pretty
        list_clouds(client, pretty)
    elif args.action == 'rename-cloud':
        cloud = choose_cloud(client, args)
        cloud.rename(args.new_name)
        print "Renamed cloud to %s" % args.new_name
    elif args.action == 'delete-cloud':
        cloud = choose_cloud(client, args)
        if cloud:
            cloud.delete()
            print "Deleted cloud %s" % cloud.title
        else:
            print "Could not find cloud"
    elif args.action == 'describe-cloud':
        cloud = choose_cloud(client, args)
        if cloud:
            show_cloud(cloud)
        else:
            print "Could not find cloud"
    elif args.action == 'add-cloud':
        add_cloud(client, args)
        print "New cloud added"
