import sys

from prettytable import PrettyTable
from mist.cmd.helpers.login import parse_config, init_client, prompt_login


def list_sizes(backend):
    sizes = backend.sizes
    x = PrettyTable(["Name", "ID"])
    for size in sizes:
        x.add_row([size['name'], size['id']])

    print x


def size_action(args):
    config = parse_config()
    if not config:
        mist_uri = "https://mist.io"
        email, password = prompt_login()
    else:
        mist_uri = config['mist_uri']
        email = config['email']
        password = config['password']

    client = init_client(mist_uri, email, password)

    backend_value = args.backend

    if args.action in ["list", "ls"] and args.target == "sizes":
        if not backend_value:
            print "You have to provide either backend name or backend id"
            sys.exit(1)
        else:
            backend = client.search_backend(backend_value)

        list_sizes(backend)