import sys
from prettytable import PrettyTable
from mist.cmd.login import parse_config, init_client, prompt_login


def list_backends(client):
    if not client.backends:
        print "No backends found"
        print
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

    if args.action == "list" and args.target == "backends":
        list_backends(client)
    elif args.action == "add" and args.target == "backend":
        title = args.name
        provider = args.provider
        key = args.key
        secret = args.secret

        client.add_backend(title=title, provider=provider, key=key, secret=secret)