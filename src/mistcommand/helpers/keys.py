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


def list_keys(client):
    if not client.keys:
        print "No keys found"
        sys.exit(0)

    x = PrettyTable(["Name", "Is Default"])
    for i in client.keys:
        key = client.keys[i]
        x.add_row([key.id, key.is_default])

    print x


def key_action(args):

    client = authenticate()

    if args.action == 'add':
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
    elif args.action == 'list':
        list_keys(client)
    elif args.action == 'delete':
        key_name = args.key
        key = client.keys[key_name]

        key.delete()
        print "Deleted %s" % key_name
    elif args.action == 'rename':
        key_name = args.key
        new_name = args.new_name

        key = client.keys[key_name]
        key.rename(new_name)
        print "Renamed key to %s" % new_name
    elif args.action == 'display':
        key_name = args.key
        key = client.keys[key_name]
        show_key(key)
