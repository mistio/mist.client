import sys

from prettytable import PrettyTable
from mist.cmd.helpers.login import authenticate


def list_providers(client):
    providers = client.supported_providers

    x = PrettyTable(["Title", "Provider ID"])
    for provider in providers:
        x.add_row([provider['title'], provider['provider']])

    print x


def provider_action(args):

    client = authenticate()

    if args.action in ["list", "ls"] and args.target in ["providers", "supported_providers"]:
        list_providers(client)
    else:
        print "Action not supported"
        sys.exit(1)