import sys

from prettytable import PrettyTable
from mistcommand.helpers.backends import return_backend
from mistcommand.helpers.login import authenticate


def list_networks(backend, pretty):
    if backend.provider not in ['openstack']:
        print "Network action not supported yet for %s provider" % backend.provider
        sys.exit(0)

    networks = backend.networks

    for network in networks:
        print "%-20s %-40s %-15s" % (network['name'], network['id'], network['status'])


def network_action(args):
    if args.action == 'list-networks':
        client = authenticate()
        backend = return_backend(client, args)
        pretty = args.pretty

        list_networks(backend, pretty)