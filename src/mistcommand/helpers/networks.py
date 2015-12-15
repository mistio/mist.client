import sys

from prettytable import PrettyTable
from mistcommand.helpers.clouds import return_cloud
from mistcommand.helpers.login import authenticate


def list_networks(cloud, pretty):
    if cloud.provider not in ['openstack']:
        print "Network action not supported yet for %s provider" % cloud.provider
        sys.exit(0)

    networks = cloud.networks

    all_nets = []
    all_nets += networks['public']
    all_nets += networks['private']

    for network in all_nets:
        print "%-20s %-40s %-15s" % (network['name'], network['id'], network['status'])


def network_action(args):
    if args.action == 'list-networks':
        client = authenticate()
        cloud = return_cloud(client, args)
        pretty = args.pretty

        list_networks(cloud, pretty)