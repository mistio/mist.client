import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def list_providers(client):
    providers = client.supported_providers

    x = PrettyTable(["Title", "Provider ID"])
    for provider in providers:
        x.add_row([provider['title'], provider['provider']])

    print x


def provider_action(args):

    client = authenticate()

    if args.action == "list":
        list_providers(client)
