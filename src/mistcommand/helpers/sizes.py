import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import choose_backend


def list_sizes(backend):
    sizes = backend.sizes
    x = PrettyTable(["Name", "ID"])
    for size in sizes:
        x.add_row([size['name'], size['id']])

    print x


def size_action(args):

    if args.action == 'list':
        client = authenticate()
        backend = choose_backend(client, args)

        list_sizes(backend)