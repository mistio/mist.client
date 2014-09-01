import sys
from prettytable import PrettyTable
from mist.cmd.login import parse_config, init_client, prompt_login


def show_backend(backend):
    x = PrettyTable(["Title", "ID", "Provider", "State"])
    x.add_row([backend.title, backend.id, backend.provider, backend.info['state']])
    print x
    print

    print "Machines:"
    x = PrettyTable(["Name", "id", "State", "Public Ips"])
    for key in backend.machines.keys():
        machine = backend.machines[key]
        try:
            public_ips = machine.info['public_ips']
            ips = " -- ".join(public_ips)
        except:
            ips = ""
        x.add_row([machine.name, machine.id, machine.info['state'], ips])
    print x


def list_backends(client):
    if not client.backends:
        print "No backends found"
        sys.exit(0)

    x = PrettyTable(["Title", "ID", "Provider", "State"])
    for id in client.backends.keys():
        backend_info = []
        backend = client.backends[id]
        backend_info.append(backend.title)
        backend_info.append(backend.id)
        backend_info.append(backend.provider)
        backend_info.append(backend.info['state'])
        x.add_row(backend_info)

    print x


def backend_action(args):
    config = parse_config()
    if not config:
        mist_uri = "https://mist.io"
        email, password = prompt_login()
    else:
        mist_uri = config['mist_uri']
        email = config['email']
        password = config['password']

    client = init_client(mist_uri, email, password)

    if args.action in ["list", "ls"] and args.target == "backends":
        list_backends(client)
    elif args.action in ["add", "create"] and args.target == "backend":
        title = args.name
        provider = args.provider
        key = args.key
        secret = args.secret
        client.add_backend(title=title, provider=provider, key=key, secret=secret)
        print "Added backend %s" % title
    elif args.action in ["delete", "remove", "rm", "del"] and args.target == "backend":
        title = args.name
        backend_id = args.id
        if title:
            backend = client.backend_from_title(title)
        elif backend_id:
            backend = client.backend_from_id(backend_id)
        else:
            print "You have to provide backend name or id"
            sys.exit(1)
        backend.delete()
        print "Deleted backend %s" % backend.title
    elif args.action == "rename" and args.target == "backend":
        title = args.name
        backend_id = args.id
        if title:
            backend = client.backend_from_title(title)
        elif backend_id:
            backend = client.backend_from_id(backend_id)
        else:
            print "You have to provide backend name or id"
            sys.exit(1)
        new_name = args.new_name
        if not new_name:
            print "You have to provide new name"
            sys.exit(1)
        backend.rename(new_name)
        print "Renamed backend %s to %s" % (backend.title, new_name)
    elif args.action in ["show", "describe", "display"] and args.target == "backend":
        title = args.name
        backend_id = args.id
        if title:
            backend = client.backend_from_title(title)
        elif backend_id:
            backend = client.backend_from_id(backend_id)
        else:
            print "You have to provide backend name or id"
            sys.exit(1)

        show_backend(backend)