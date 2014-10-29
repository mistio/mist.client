import sys

from prettytable import PrettyTable
from mistcommand.helpers.backends import choose_backend
from mistcommand.helpers.login import authenticate

def list_locations(backend):
    locations = backend.locations
    x = PrettyTable(["Name", "ID"])
    for location in locations:
        x.add_row([location['name'], location['id']])

    print x


def location_action(args):

    if args.action == 'list':
        client = authenticate()
        backend = choose_backend(client, args)
        list_locations(backend)