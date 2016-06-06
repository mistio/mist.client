import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.clouds import return_cloud


def choose_machines_by_tag(client, tag):
    chosen_machines = []
    machines = client.machines()
    for machine in machines:
        machine_tags = machine.info.get('tags', [])
        if tag in machine_tags:
            chosen_machines.append(machine)
    return chosen_machines


def clean_tags(tags):
    _tags = []
    if not tags:
        return '-'
    for tag in tags:
        for key, value in tag.iteritems():
            tag_pair = '%s=%s' % (key, value)
            _tags.append(tag_pair)
    return ', '.join(_tags)


def parsed_probe(info):
    load = info['loadavg']
    output = ''
    output += 'LOAD: %s/%s/%s' % (load[0], load[1], load[2])
    output += 'PING: %s/%s/%s' % (info['rtt_min'], info['rtt_avg'], info['rtt_max'])
    return output


def list_machines(client, cloud, pretty):
    x = PrettyTable(["Name", "ID", "State", "Public Ips", "Cloud Title", "Tags"])
    if not cloud:
        machines = client.machines()
        for machine in machines:
            try:
                public_ips = machine.info['public_ips']
                ips = " -- ".join(public_ips)
            except:
                ips = ""
            machine_tags = machine.info.get('tags', '')
            machine_tags = clean_tags(machine_tags)
            # try:
            #     tags = machine_tags
            # except:
            #     tags = []
            if pretty:
                x.add_row([machine.name, machine.id, machine.info['state'],
                           ips, machine.cloud.title, machine_tags])
            else:
                print "%-25s %-60s %-10s %-20s %-30s %-20s" % (machine.name,
                                                               machine.id,
                                                               machine.info['state'],
                                                               ips,
                                                               machine.cloud.title,
                                                               machine_tags)
    else:
        machines = cloud.machines()
        for machine in machines:
            try:
                public_ips = machine.info['public_ips']
                ips = " -- ".join(public_ips)
            except:
                ips = ""
            machine_tags = machine.info.get('tags', '')
            machine_tags = clean_tags(machine_tags)
            # tags = ",".join(machine_tags)
            if pretty:
                x.add_row([machine.name, machine.id, machine.info['state'],
                           ips, cloud.title, machine_tags])
            else:
                print "%-25s %-60s %-10s %-20s %-30s %-20s" % (machine.name,
                                                               machine.id,
                                                               machine.info['state'],
                                                               ips,
                                                               machine.cloud.title,
                                                               machine_tags)
    if pretty:
        print x


def display_machine(machine):
    x = PrettyTable(["Name", "ID", "State", "Public Ips", "Cloud Title", "Tags"])

    try:
        public_ips = machine.info['public_ips']
        ips = " -- ".join(public_ips)
    except:
        ips = ""

    machine_tags = machine.info.get('tags', '')
    machine_tags = clean_tags(machine_tags)

    x.add_row([machine.name, machine.id, machine.info['state'],
               ips, machine.cloud.title, machine_tags])
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
            print "Short probe output for machine %s:" % machine.name
            print parsed_probe(info)
        else:
            print "Machine could not be probed successfully" % machine.name


def choose_machine(client, args):
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


def create_machine(client, cloud, args):
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
    cloud.create_machine(name=name, key=key, image_id=image_id, size_id=size_id,
                         location_id=location_id, networks=networks, script_id=args.script_id,
                         script_params=args.script_params, monitoring=args.monitoring)


def machine_action(args):

    client = authenticate()

    if args.action == 'list-machines':
        if args.cloud or args.cloud_id or args.cloud_name:
            cloud = return_cloud(client, args)
        else:
            cloud = None

        pretty = args.pretty

        list_machines(client, cloud, pretty)

    elif args.action == 'describe-machine':
        machine = choose_machine(client, args)
        display_machine(machine)

    elif args.action == 'create-machine':
        cloud = return_cloud(client, args)
        create_machine(client, cloud, args)
        print "Created machine %s" % args.machine_name

    elif args.action in ['start', 'stop', 'reboot', 'destroy', 'probe']:
        machine = choose_machine(client, args)
        if not machine:
            print "Cannot find machine"
            sys.exit(0)
        try:
            machine_take_action(machine, args.action)
        except:
            print "Failed to execute %s action on %s " % (args.action, machine)
            sys.exit(0)

    elif args.action == 'enable-monitoring':
        machine = choose_machine(client, args)
        machine.enable_monitoring()
        print "Enabled monitoring to machine %s" % machine.name

    elif args.action == 'disable-monitoring':
        machine = choose_machine(client, args)
        machine.disable_monitoring()
        print "Disabled monitoring to machine %s" % machine.name

    elif args.action in ['add-tag', 'remove-tag']:
        machine = choose_machine(client, args)
        if machine.info['can_tag']:
            if args.action == 'add-tag':
                machine.add_tag(key=args.key, value=args.value)
                print "Added tag %s=%s to machine %s" % (args.key,
                                                         args.value,
                                                         machine.name)
            elif args.action == 'remove-tag':
                machine.del_tag(key=args.key, value=args.value)
                print "Removed tag %s=%s from machine %s" % (args.key,
                                                             args.value,
                                                             machine.name)
            else:
                "Unknown action to be performed on machine tags"
                sys.exit(0)
        else:
            print "Cannot tag machine on provider %s" % machine.cloud.title
            sys.exit(0)
