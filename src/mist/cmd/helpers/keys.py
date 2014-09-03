import sys

from prettytable import PrettyTable
from mist.cmd.helpers.login import authenticate


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

    if args.action in ["list", "ls"] and args.target == "keys":
        list_keys(client)
    elif args.action in ["add", "create"] and args.target == "key":
        name = args.name
        key = args.key

        if args.auto:
            private = client.generate_key()

        else:
            with open(key, "r") as f:
                private = f.read().strip("\n")

        client.add_key(key_name=name, private=private)
        print "Added key %s" % name
    elif args.action in ["delete", "remove", "rm", "del"] and args.target == "key":
        key_name = args.name
        if not key_name:
            print "You have to provide key name"
            sys.exit(1)
        key = client.keys[key_name]
        key.delete()
        print "Deleted key %s" % key_name
    elif args.action == "rename" and args.target == "key":
        key_name = args.name
        if not key_name:
            print "You have to provide key name"
            sys.exit(1)

        new_name = args.new_name
        if not new_name:
            print "You have to provide new name for the key"
            sys.exit(1)

        key = client.keys[key_name]
        key.rename(new_name)
        print "Renamed %s to %s" % (key_name, new_name)
    elif args.action in ["show", "describe", "display"] and args.target == "key":
        key_name = args.name
        if not key_name:
            print "You have to provide key name"
            sys.exit(1)

        key = client.keys[key_name]
        show_key(key)
    else:
        print "Action not supported"
        sys.exit(1)