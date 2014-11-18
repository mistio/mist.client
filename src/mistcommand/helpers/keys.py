import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def show_key(key):
    print "Name: %s" % key.id
    print

    print "Private key:"
    print key.private
    print

    print "Puclic key:"
    print key.public


def list_keys(client, pretty):
    keys = client.keys()
    if not keys:
        print "No keys found"
        sys.exit(0)

    if pretty:
        x = PrettyTable(["Name", "Is Default"])
        for key in keys:
            x.add_row([key.id, key.is_default])

        print x
    else:
        for key in keys:
            print "%s" % key.id


def key_action(args):

    client = authenticate()

    if args.action == 'add-key':
        name = args.name
        key_path = args.key_path
        auto = args.auto_generate

        if auto:
            private = client.generate_key()
        else:
            with open(key_path, "r") as f:
                private = f.read().strip("\n")

        client.add_key(key_name=name, private=private)
        print "Added key %s" % name
    elif args.action == 'list-keys':
        pretty = args.pretty
        list_keys(client, pretty)
    elif args.action == 'delete-key':
        key_id = args.key_name if args.key_name else args.key_id
        keys = client.keys(id=key_id)
        key = keys[0] if keys else None
        if key:
            key.delete()
            print "Deleted %s" % key.id
        else:
            print "Cound not find key: %s" % args.key
            sys.exit(0)
    elif args.action == 'rename-key':
        key_name = args.key_name if args.key_name else args.key_id
        new_name = args.new_name

        keys = client.keys(id=key_name)
        key = keys[0] if keys else None

        if key:
            key.rename(new_name)
            print "Renamed key to %s" % new_name
        else:
            print "Could not find key: %s" % key_name
    elif args.action == 'describe-key':
        key_name = args.key_name if args.key_name else args.key_id
        keys = client.keys(id=key_name)
        key = keys[0] if keys else None
        if key:
            show_key(key)
        else:
            print "Could not find key: %s" % key_name

