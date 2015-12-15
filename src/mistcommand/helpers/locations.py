import sys

from prettytable import PrettyTable
from mistcommand.helpers.clouds import return_cloud
from mistcommand.helpers.login import authenticate


def list_locations(cloud, pretty):
    locations = cloud.locations

    if pretty:
        x = PrettyTable(["Name", "ID"])
        for location in locations:
            x.add_row([location['name'], location['id']])

        print x
    else:
        for location in locations:
            print "%-20s %-20s" % (location['name'], location['id'])


def location_action(args):

    if args.action == 'list-locations':
        client = authenticate()
        cloud = return_cloud(client, args)
        pretty = args.pretty

        list_locations(cloud, pretty)