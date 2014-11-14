import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import return_backend


def list_sizes(backend, pretty):
    sizes = backend.sizes

    if pretty:
        x = PrettyTable(["Name", "ID"])
        for size in sizes:
            x.add_row([size['name'], size['id']])

        print x
    else:
        for size in sizes:
            print "%-20s %-20s" % (size['name'], size['id'])


def size_action(args):

    if args.action == 'list-sizes':
        client = authenticate()
        backend = return_backend(client, args)

        pretty = args.pretty
        list_sizes(backend, pretty)