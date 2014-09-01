import sys

from prettytable import PrettyTable
from mist.cmd.helpers.login import parse_config, init_client, prompt_login


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


def toggle_monitoring(machine, action):
    if action == "enable-monitoring":
        machine.enable_monitoring()
        print "Enabled monitoring to machine %s" % machine.name
    else:
        machine.disable_monitoring()
        print "Disabled monitoring from machine %s" % machine.name


def list_plugins(machine):
    plugins = machine.available_metrics

    x = PrettyTable(["Plugin Name", "Plugin ID"])

    for key in plugins.keys():
        plugin = plugins[key]
        x.add_row([plugin['name'], key])

    print x


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

        for arg in [args.name, args.image, args.size, args.key, args.location]:
            if not arg:
                print "You have to provide name, image id, size id, location id, size id and key id"
                sys.exit(1)

        name = args.name
        key = client.keys[args.key]
        image_id = args.image
        size_id = args.size
        location_id = args.location

        backend.create_machine(name=name, key=key, image_id=image_id, location_id=location_id, size_id=size_id)
        print "Created machine %s" % name
    elif args.action in ["enable-monitoring", "disable-monitoring"] and args.target == "machine":
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

        toggle_monitoring(machine, args.action)
    elif args.action in ["list", "ls"] and args.target == "plugins":
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

        list_plugins(machine)
    elif args.action in ["add", "create"] and args.target == "plugin":
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

        if not args.plugin:
            print "You have to provide plugin id or name"
            sys.exit(1)
        else:
            plugin_id = args.plugin

            if not args.custom_plugin:
                machine.add_metric(plugin_id)
                print "Added Plugin %s to monitored machine %s" % (plugin_id, machine.name)
            else:
                machine.add_python_plugin(name=plugin_id, python_file=args.custom_plugin)
                print "Added %s file as custom plugin" % args.custom_plugin