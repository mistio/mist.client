import sys
from prettytable import PrettyTable
from mist.cmd.login import parse_config, init_client, prompt_login


def list_providers(client):
    providers = client.supported_providers

    x = PrettyTable(["Title", "Provider ID"])
    for provider in providers:
        x.add_row([provider['title'], provider['provider']])

    print x


def provider_action(args):
    config = parse_config()
    if not config:
        mist_uri = "https://mist.io"
        email, password = prompt_login()
    else:
        mist_uri = config['mist_uri']
        email = config['email']
        password = config['password']

    client = init_client(mist_uri, email, password)

    if args.action in ["list", "ls"] and args.target in ["providers", "supported_providers"]:
        list_providers(client)
    else:
        print "Action not supported"
        sys.exit(1)