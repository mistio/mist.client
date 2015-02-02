import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def show_backend(backend):
    x = PrettyTable(["Title", "ID", "Provider", "State"])
    x.add_row([backend.title, backend.id, backend.provider, backend.info['state']])
    print x
    print

    print "Machines:"
    x = PrettyTable(["Name", "ID", "State", "Public Ips"])
    machines = backend.machines()

    for machine in machines:
        try:
            public_ips = machine.info['public_ips']
            ips = " -- ".join(public_ips)
        except:
            ips = ""
        x.add_row([machine.name, machine.id, machine.info['state'], ips])

    print x


def list_backends(client, pretty):
    backends = client.backends()
    if not client.backends():
        print "No backends found"
        sys.exit(0)

    if pretty:
        x = PrettyTable(["Name", "ID", "Provider", "State"])
        for backend in backends:
            x.add_row([backend.title, backend.id, backend.provider, backend.info['state']])

        print x
    else:
        for backend in backends:
            # print backend.title, backend.id, backend.provider, backend.info['state']
            print "%-40s %-40s %-30s %-20s" % (backend.title, backend.id, backend.provider, backend.info['state'])


def choose_backend(client, args):
    backend_id = args.id
    backend_name = args.name
    if backend_id:
        backends = client.backends(id=backend_id) or None
        backend = backends[0] if backends else None
    elif backend_name:
        backends = client.backends(name=backend_name)
        backend = backends[0] if backends else None
    else:
        backends = client.backends(search=args.backend)
        backend = backends[0] if backends else None

    return backend


def return_backend(client, args):
    backend_id = args.backend_id
    backend_name = args.backend_name
    if backend_id:
        backends = client.backends(id=backend_id) or None
        backend = backends[0] if backends else None
    elif backend_name:
        backends = client.backends(name=backend_name)
        backend = backends[0] if backends else None
    else:
        backends = client.backends(search=args.backend)
        backend = backends[0] if backends else None

    return backend


def add_backend(client, args):
    provider = args.provider
    if "ec2" in provider:
        add_ec2_backend(client, args)
    elif "rackspace" in provider:
        add_rackspace_backend(client, args)
    elif "nepho" in provider:
        add_nepho_backend(client, args)
    elif "digi" in provider:
        add_digital_backend(client,args)
    elif "linode" in provider:
        add_linode_backend(client, args)
    elif "openstack" in provider:
        add_openstack_backend(client, args)
    elif "softlayer" in provider:
        add_softlayer_backend(client, args)
    elif "hp" in provider:
        add_hp_backend(client, args)
    elif "docker" in provider:
        add_docker_backend(client, args)
    elif "azure" in provider:
        add_azure_backend(client, args)
    elif "bare" in provider:
        add_bare_metal_backend(client, args)
    elif "gce" in provider:
        add_gce_backend(client, args)
    elif provider == "vcloud":
        add_vcloud_backend(client, args)
    elif provider == "indonesian_vcloud":
        add_indonesian_backend(client, args)
    elif provider == "libvirt":
        add_libvirt_backend(client, args)


def add_gce_backend(client, args):
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

    client.add_backend(title=title, provider=provider, email=email, project_id=project_id,
                       private_key=private_key)


def add_libvirt_backend(client, args):
    title = args.name
    provider = args.provider

    machine_hostname = args.libvirt_hostname
    machine_user = args.libvirt_user
    machine_key = args.libvirt_key

    client.add_backend(title=title, provider=provider, machine_hostname=machine_hostname, machine_user=machine_user,
                       machine_key=machine_key)


def add_vcloud_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.vcloud_username
    password = args.vcloud_password
    organization = args.vcloud_organization
    host = args.vcloud_host

    client.add_backend(title=title, provider=provider, username=username, password=password,
                       organization=organization, host=host)


def add_indonesian_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.indonesian_username
    password = args.indonesian_password
    organization = args.indonesian_organization

    client.add_backend(title=title, provider=provider, username=username, password=password,
                       organization=organization)


def add_docker_backend(client, args):
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

    client.add_backend(title=title, provider=provider, docker_host=docker_host, docker_port=docker_port,
                       auth_user=docker_auth_user, auth_password=docker_auth_password, key_file=key_file,
                       cert_file=cert_file)


def add_azure_backend(client, args):
    title = args.name
    provider = args.provider

    subscription_id = args.azure_sub_id
    with open(args.azure_cert_path) as f:
        certificate = f.read()

    client.add_backend(title=title, provider=provider, subscription_id=subscription_id, certificate=certificate)


def add_ec2_backend(client, args):
    title = args.name
    provider = args.provider

    api_key = args.ec2_api_key
    api_secret = args.ec2_api_secret
    region = args.ec2_region

    client.add_backend(title=title, provider=provider, api_key=api_key, api_secret=api_secret, region=region)


def add_rackspace_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.rackspace_username
    api_key = args.rackspace_api_key
    region = args.rackspace_region

    client.add_backend(title=title, provider=provider, username=username, api_key=api_key, region=region)


def add_nepho_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.nepho_username
    password = args.nepho_password

    client.add_backend(title=title, provider=provider, username=username, password=password)


def add_digital_backend(client, args):
    title = args.name
    provider = args.provider

    token = args.digi_token

    client.add_backend(title=title, provider=provider, token=token)


def add_linode_backend(client, args):
    title = args.name
    provider = args.provider

    api_key = args.linode_api_key

    client.add_backend(title=title, provider=provider, api_key=api_key)


def add_openstack_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.openstack_username
    password = args.openstack_password
    auth_url = args.openstack_auth_url
    tenant_name = args.openstack_tenant
    region = args.openstack_region

    client.add_backend(title=title, provider=provider, username=username, password=password,
                       auth_url=auth_url, tenant_name=tenant_name, region=region)


def add_softlayer_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.softlayer_username
    api_key = args.softlayer_api_key

    client.add_backend(title=title, provider=provider, username=username, api_key=api_key)


def add_hp_backend(client, args):
    title = args.name
    provider = args.provider

    username = args.hp_username
    password = args.hp_password
    tenant_name = args.hp_tenant
    region = args.hp_region

    client.add_backend(title=title, provider=provider, username=username, password=password, tenant_name=tenant_name,
                       region=region)


def add_bare_metal_backend(client, args):
    title = args.name
    provider = args.provider

    machine_ip = args.bare_hostname
    machine_user = args.bare_user

    machine_port = args.bare_port
    machine_key = args.bare_ssh_key_id

    client.add_backend(title=title, provider=provider, machine_ip=machine_ip, machine_key=machine_key,
                       machine_port=machine_port, machine_user=machine_user)


def backend_action(args):

    client = authenticate()

    if args.action == 'list-backends':
        pretty = args.pretty
        list_backends(client, pretty)
    elif args.action == 'rename-backend':
        backend = choose_backend(client, args)
        backend.rename(args.new_name)
        print "Renamed backend to %s" % args.new_name
    elif args.action == 'delete-backend':
        backend = choose_backend(client, args)
        if backend:
            backend.delete()
            print "Deleted backend %s" % backend.title
        else:
            print "Could not find backend"
    elif args.action == 'describe-backend':
        backend = choose_backend(client, args)
        if backend:
            show_backend(backend)
        else:
            print "Could not find backend"
    elif args.action == 'add-backend':
        add_backend(client, args)
        print "New backend added"
