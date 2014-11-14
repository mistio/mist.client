import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def list_providers(client, pretty):
    providers = client.supported_providers

    if pretty:
        x = PrettyTable(["Title", "Provider ID"])
        for provider in providers:
            x.add_row([provider['title'], provider['provider']])

        print x
    else:
        for provider in providers:
            print "%-30s %-20s" % (provider['title'], provider['provider'])


def provider_action(args):

    client = authenticate()

    if args.action == "list-providers":
        pretty = args.pretty
        list_providers(client,pretty)
