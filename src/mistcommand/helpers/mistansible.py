import ansible

from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import choose_machines_by_tag


def ansible_action(args):
    client = authenticate()
    tag = args.tag

    machines = choose_machines_by_tag(client, tag)
    print machines
