from prettytable import PrettyTable

from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import choose_backend
from mistcommand.helpers.machines import choose_machine


def list_plugins(machine):
    plugins = machine.available_metrics

    x = PrettyTable(["Plugin Name", "Plugin ID"])

    for key in plugins.keys():
        plugin = plugins[key]
        x.add_row([plugin['name'], key])

    print x


def plugin_action(args):

    client = authenticate()

    if args.action == 'list':
        backend = choose_backend(client, args)
        machine = choose_machine(backend, args)

        list_plugins(machine)
    elif args.action == 'add':
        backend = choose_backend(client, args)
        machine = choose_machine(backend, args)

        machine.add_metric(args.plugin_id)
        print "Added Plugin %s to monitored machine %s" % (args.plugin_id, machine.name)