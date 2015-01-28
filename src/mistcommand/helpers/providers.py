import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def list_providers(client, pretty):
    providers = client.supported_providers

    if pretty:
        x = PrettyTable(["Provider", "Provider ID", "Region", "Region ID"])
        for provider in providers:
            if provider['regions']:
                for region in provider['regions']:
                    x.add_row([provider['title'], provider['provider'], region['location'], region['id']])
            else:
                x.add_row([provider['title'], provider['provider'], '-', '-'])

        print x
    else:
        for provider in providers:
            if provider['regions']:
                for region in provider['regions']:
                    print "%-30s %-20s %-20s %-20s" % \
                          (provider['title'], provider['provider'], region['location'], region['id'])
            else:
                print "%-30s %-20s" % (provider['title'], provider['provider'])


def provider_action(args):

    client = authenticate()

    if args.action == "list-providers":
        pretty = args.pretty
        list_providers(client,pretty)
