import sys
from prettytable import PrettyTable
from mist.cmd.login import parse_config, init_client, prompt_login


def list_keys(client):
    if not client.keys:
        print "No keys found"
        print
        sys.exit(0)

    x = PrettyTable(["Name", "Is Default"])
    for i in client.keys:
        key = client.keys[i]
        x.add_row([key.id, key.is_default])

    print x
    print


def key_action(args):
    config = parse_config()
    if not config:
        mist_uri = "https://mist.io"
        email, password = prompt_login()
    else:
        mist_uri = config['mist_uri']
        email = config['email']
        password = config['password']

    client = init_client(mist_uri, email, password)

    if args.action == "list" and args.target == "keys":
        list_keys(client)
    elif args.action == "add" and args.target == "key":
        name = args.name
        key = args.key

        if args.auto:
            private = client.generate_key()

        else:
            with open(key, "r") as f:
                private = f.read().strip("\n")

        client.add_key(key_name=name, private=private)
        print "Added key %s" % name
        print
    elif args.action == "delete" and args.target == "backend":
        title = args.name
        backend_id = args.id
        if title:
            backend = client.backend(title)
        elif backend_id:
            backend = client.backend(backend_id)
        else:
            print "You have to provide backend name or id"
            print
            sys.exit(1)
        backend.delete()
        print "Deleted backend %s" % backend.title
        print