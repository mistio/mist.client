from prettytable import PrettyTable

from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import return_machine


def list_metrics(machine, pretty):
    plugins = machine.available_metrics

    x = PrettyTable(["Metric Name", "Metric ID"])

    if pretty:
        for key in plugins.keys():
            plugin = plugins[key]
            x.add_row([plugin['name'], key])

        print x
    else:
        for key in plugins.keys():
            plugin = plugins[key]
            print "%-50s %-20s" % (plugin['name'], key)


def metric_action(args):

    client = authenticate()

    if args.action == 'list-metrics':
        machine = return_machine(client, args)
        pretty = args.pretty
        list_metrics(machine, pretty)
    elif args.action == 'add-metric':
        machine = return_machine(client, args)

        machine.add_metric(args.metric_id)
        print "Added Metric %s to monitored machine %s" % (args.metric_id, machine.name)
    elif args.action == 'add-custom-metric':
        machine = return_machine(client, args)
        name = args.metric_name
        python_file = args.file_path
        value_type = args.value_type
        unit = args.unit

        machine.add_python_plugin(name, python_file, value_type, unit)

        print "Added custom metric %s" % name