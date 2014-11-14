import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import return_backend


def choose_machines_by_tag(client, tag):
    chosen_machines = []
    machines = client.machines()

    for machine in machines:
        machine_tags = machine.info.get('tags', [])
        if tag in machine_tags:
            chosen_machines.append(machine)

    return chosen_machines


def list_machines(client, backend, pretty):
    x = PrettyTable(["Name", "ID", "State", "Public Ips", "Backend Title", "Tags"])
    if not backend:
        machines = client.machines()
        for machine in machines:
            try:
                public_ips = machine.info['public_ips']
                ips = " -- ".join(public_ips)
            except:
                ips = ""
            machine_tags = machine.info.get('tags', [])
            tags = ",".join(machine_tags)

            if pretty:
                x.add_row([machine.name, machine.id, machine.info['state'], ips, machine.backend.title, tags])
            else:
                print "%-25s %-60s %-10s %-20s %-30s %-20s" % (machine.name, machine.id, machine.info['state'], ips,
                                                               machine.backend.title, tags)

    else:
        machines = backend.machines()
        for machine in machines:
            try:
                public_ips = machine.info['public_ips']
                ips = " -- ".join(public_ips)
            except:
                ips = ""
            machine_tags = machine.info.get('tags', [])
            tags = ",".join(machine_tags)
            if pretty:
                x.add_row([machine.name, machine.id, machine.info['state'], ips, backend.title, tags])
            else:
                print "%-25s %-60s %-10s %-20s %-30s %-20s" % (machine.name, machine.id, machine.info['state'], ips,
                                                               machine.backend.title, tags)

    if pretty:
        print x


def display_machine(machine):
    x = PrettyTable(["Name", "ID", "State", "Public Ips", "Backend Title", "Tags"])

    try:
        public_ips = machine.info['public_ips']
        ips = " -- ".join(public_ips)
    except:
        ips = ""

    machine_tags = machine.info.get('tags', [])
    tags = ",".join(machine_tags)

    x.add_row([machine.name, machine.id, machine.info['state'], ips, machine.backend.title, tags])
    print x


def machine_take_action(machine, action):
    if action == "start":
        machine.start()
        print "Started machine %s" % machine.name
    elif action == "stop":
        machine.stop()
        print "Stopped machine %s" % machine.name
    elif action == "reboot":
        machine.reboot()
        print "Rebooted machine %s" % machine.name
    elif action == "destroy":
        machine.destroy()
        print "Destroyed machine %s" % machine.name
    elif action == "probe":
        info = machine.probe()
        if "uptime" in info.keys():
            print "Machine %s is probed" % machine.name
        else:
            print "Not probed"


def choose_machine(client, args):
    machine_id = args.id
    machine_name = args.name
    if machine_id:
        machines = client.machines(id=machine_id)
        machine = machines[0] if machines else None
    elif machine_name:
        machines = client.machines(name=machine_name)
        machine = machines[0] if machines else None
    else:
        machines = client.machines(search=args.machine)
        machine = machines[0] if machines else None

    return machine


def return_machine(client, args):
    machine_id = args.machine_id
    machine_name = args.machine_name
    if machine_id:
        machines = client.machines(id=machine_id)
        machine = machines[0] if machines else None
    elif machine_name:
        machines = client.machines(name=machine_name)
        machine = machines[0] if machines else None
    else:
        machines = client.machines(search=args.machine)
        machine = machines[0] if machines else None

    return machine


def create_machine(client, backend, args):
    keys = client.keys(id=args.key_id)
    key = keys[0] if keys else None

    if not key:
        print "Could not find key: %s" % args.key_id
        sys.exit(1)

    name = args.machine_name
    image_id = args.image_id
    size_id = args.size_id
    location_id = args.location_id
    networks = []
    if args.network_id:
        networks.append(args.network_id)

    backend.create_machine(name=name, key=key, image_id=image_id, size_id=size_id, location_id=location_id,
                           networks=networks)


def machine_action(args):

    client = authenticate()

    if args.action == 'list-machines':
        if args.backend or args.backend_id or args.backend_name:
            backend = return_backend(client, args)
        else:
            backend = None

        pretty = args.pretty

        list_machines(client, backend, pretty)

    elif args.action == 'describe-machine':
        machine = choose_machine(client, args)

        display_machine(machine)

    elif args.action == 'create-machine':
        backend = return_backend(client, args)
        create_machine(client, backend, args)
        print "Created machine %s" % args.machine_name

    elif args.action in ['start', 'stop', 'reboot', 'destroy', 'probe']:
        machine = choose_machine(client, args)

        machine_take_action(machine, args.action)
    elif args.action == 'enable-monitoring':
        machine = choose_machine(client, args)
        machine.enable_monitoring()
        print "Enabled monitoring to machine %s" % machine.name

    elif args.action == 'disable-monitoring':
        machine = choose_machine(client, args)
        machine.disable_monitoring()
        print "Disabled monitoring to machine %s" % machine.name

    elif args.action == 'tag':
        machine = choose_machine(client, args)

        if machine.info['can_tag']:
            machine.tag(tag=args.new_tag)
            print "Add tag %s to machine %s" % (args.new_tag, machine.name)
        else:
            print "Cannot tag machine on provider %s" % machine.backend.title
            sys.exit(0)