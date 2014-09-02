import sys

from prettytable import PrettyTable
from mist.cmd.helpers.login import authenticate


def list_locations(backend):
    locations = backend.locations
    x = PrettyTable(["Name", "ID"])
    for location in locations:
        x.add_row([location['name'], location['id']])

    print x


def location_action(args):

    client = authenticate()

    backend_value = args.backend

    if args.action in ["list", "ls"] and args.target == "locations":
        if not backend_value:
            print "You have to provide either backend name or backend id"
            sys.exit(1)
        else:
            backend = client.search_backend(backend_value)

        list_locations(backend)