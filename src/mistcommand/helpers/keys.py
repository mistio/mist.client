import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import choose_machine


def show_key(key):
    print "Name: %s" % key.name
    print "ID: %s" % key.id
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
        x = PrettyTable(["ID", "Name", "Is Default"])
        for key in keys:
            x.add_row([key.id, key.name, key.is_default])

        print x
    else:
        for key in keys:
            print "%-40s %-30s %-20s" % (key.id, key.name, key.is_default)


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
            print "Deleted %s (%s)" % (key.name, key.id)
        else:
            print "Could not find key: %s" % args.key
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
    elif args.action == 'associate-key':
        machine = choose_machine(client, args)
        key_name = args.key
        print "Attempting to deploy key to machine over SSH ..."
        keys = client.keys(id=key_name)
        key = keys[0] if keys else None
        if machine and key:
            cloud_id = machine.cloud.id
            machine_id = machine.id
            ips = [ip for ip in machine.info['public_ips'] if ':' not in ip]
            host = ips[0]
            key.associate(cloud_id, machine_id, host)
            print "Successfully associated key %s to machine %s" % (key.id,
                                                                    machine.name)
        else:
            print "Key association failed"
    elif args.action == 'disassociate-key':
        machine = choose_machine(client, args)
        key_name = args.key
        keys = client.keys(id=key_name)
        key = keys[0] if keys else None
        if machine and key:
            cloud_id = machine.cloud.id
            machine_id = machine.id
            ips = [ip for ip in machine.info['public_ips'] if ':' not in ip]
            host = ips[0]
            if host:
                print "Attempting to remove key from machine ..."
            key.disassociate(cloud_id, machine_id, host)
            print "Successfully disassociated key-machine " \
                  "(%s-%s) pair" % (key.id, machine.name)
        else:
            print "Key disassociation failed"
            sys.exit(1)
