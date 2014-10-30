import time
import os
import sys
import tempfile

from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import choose_machines_by_tag


def update_key_association(client, machines):
    keys = client.keys
    machine_ids = [machine.id for machine in machines]

    for key_id in keys.keys():
        assoc_machines = keys[key_id].info['machines']
        for assoc_machine in assoc_machines:
            id = assoc_machine[1]
            if id in machine_ids:
                for machine in machines:
                    if machine.id == id:
                        print "Found key associoation for machine: %s" % machine.name
                        machine.info['assoc'] = {
                            'key_id': key_id,
                            'user': assoc_machine[3]
                        }

    return machines


def ansible_action(args, Runner, Inventory):
    client = authenticate()
    tag = args.tag

    machines = choose_machines_by_tag(client, tag)
    if not machines:
        print "No machines found with tag: %s" % tag
        sys.exit(0)
    else:
        print "Found tagged machines"


    machines = update_key_association(client, machines)
    assoc_machines = [machine for machine in machines if machine.info.get('assoc', None)]
    print assoc_machines

