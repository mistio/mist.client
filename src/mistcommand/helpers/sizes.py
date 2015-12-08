import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.clouds import return_cloud


def list_sizes(cloud, pretty):
    sizes = cloud.sizes

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
        cloud = return_cloud(client, args)

        pretty = args.pretty
        list_sizes(cloud, pretty)