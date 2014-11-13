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
        print "Not implemented yet"
        sys.exit(0)
    elif "bare" in provider:
        add_bare_metal_backend(client, args)


def add_ec2_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.ec2_api_key
    secret = args.ec2_api_secret

    client.add_backend(title=title, provider=provider, key=key, secret=secret)


def add_rackspace_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.rackspace_username
    secret = args.rackspace_api_key

    client.add_backend(title=title, provider=provider, secret=secret, key=key)


def add_nepho_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.nepho_username
    secret = args.nepho_password

    client.add_backend(title=title, provider=provider, secret=secret, key=key)


def add_digital_backend(client, args):
    title = args.name
    provider = args.provider

    key = "dummy"
    secret = args.digi_token

    client.add_backend(title=title, provider=provider, secret=secret, key=key)


def add_linode_backend(client, args):
    title = args.name
    provider = args.provider

    key = "dummy"
    secret = args.linode_api_key

    client.add_backend(title=title, provider=provider, secret=secret, key=key)


def add_openstack_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.openstack_username
    secret = args.openstack_password
    apiurl = args.openstack_auth_url
    tenant_name = args.openstack_tenant
    region = args.openstack_region

    client.add_backend(title=title, provider=provider, key=key, secret=secret, apiurl=apiurl,
                       tenant_name=tenant_name, region=region)


def add_softlayer_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.softlayer_username
    secret = args.softlayer_api_key

    client.add_backend(title=title, provider=provider, secret=secret, key=key)


def add_hp_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.hp_username
    secret = args.hp_password
    tenant_name = args.hp_tenant

    client.add_backend(title=title, provider=provider, secret=secret, key=key, tenant_name=tenant_name)


def add_bare_metal_backend(client, args):
    title = args.name
    provider = args.provider

    key = args.bare_hostname
    secret = args.bare_user

    machine_port = args.bare_port
    machine_key = args.bare_ssh_key_id

    client.add_backend(title=title, provider=provider, secret=secret, key=key, machine_key=machine_key,
                       machine_port=machine_port, machine_user=secret)


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
    elif args.action == 'display':
        backend = choose_backend(client, args)
        if backend:
            show_backend(backend)
        else:
            print "Could not find backend"
    elif args.action == 'add':
        add_backend(client, args)
        print "New backend added"
