import sys
from prettytable import PrettyTable
from mist.cmd.login import parse_config, init_client, prompt_login


def list_machines(client, backend_value):
    x = PrettyTable(["Name", "ID", "State", "Public Ips", "Backend Title"])
    if not backend_value:
        backends = client.backends
        for i in backends.keys():
            backend = backends[i]
            machines = backend.machines
            for y in machines.keys():
                machine = machines[y]
                try:
                    public_ips = machine.info['public_ips']
                    ips = " -- ".join(public_ips)
                except:
                    ips = ""
                x.add_row([machine.name, machine.id, machine.info['state'], ips, backend.title])
    else:
        backend = client.search_backend(backend_value)
        machines = backend.machines
        for y in machines.keys():
            machine = machines[y]
            try:
                public_ips = machine.info['public_ips']
                ips = " -- ".join(public_ips)
            except:
                ips = ""
            x.add_row([machine.name, machine.id, machine.info['state'], ips, backend.title])

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
            print "Uptime: %s" % info['uptime']
        else:
            print "Not probed"


def machine_action(args):
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
    if args.action in ["list", "ls"] and args.target == "machines":
        list_machines(client, backend_value)
    elif args.action in ["start", "stop", "destroy", "reboot", "probe"] and args.target == "machine":
        if not backend_value:
            print "You have to provide either backend name or backend id"
            sys.exit(1)
        else:
            backend = client.search_backend(backend_value)

        machine_name = args.name
        machine_id = args.id
        if machine_name:
            machine = backend.machine_from_name(machine_name)
        elif machine_id:
            machine = backend.machine_from_id(machine_id)
        else:
            print "You have to provide either machine name or machine id"
            sys.exit(1)
        machine_take_action(machine, args.action)
    elif args.action in ["create", "add"] and args.target == "machine":
        if not backend_value:
            print "You have to provide either backend name or backend id"
            sys.exit(1)
        else:
            backend = client.search_backend(backend_value)


