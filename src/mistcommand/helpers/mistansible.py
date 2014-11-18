import os
import sys
import tempfile
import shutil

from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import choose_machines_by_tag


def update_key_association(client, machines):
    keys = client.keys()
    machine_ids = [machine.id for machine in machines]
    assoc_keys = []

    for key in keys:
        assoc_machines = key.info['machines']
        for assoc_machine in assoc_machines:
            id = assoc_machine[1]
            if id in machine_ids:
                for machine in machines:
                    if machine.id == id:
                        print "Found key association for machine: %s" % machine.name
                        machine.info['assoc'] = {
                            'key_id': key.id,
                            'user': assoc_machine[3],
                            'port': assoc_machine[-1]
                        }
                        assoc_keys.append(key)

    return machines, assoc_keys


def init_ansible_tmp_dir(assoc_machines, assoc_keys, tag):
    tmp_dir = tempfile.mkdtemp()
    tmp_ansible_host_file = os.path.join(tmp_dir, 'mist_ansible_hosts')

    # Save the ssh private keys
    for key in assoc_keys:
        key_file = os.path.join(tmp_dir, key.id)
        with open(key_file, 'w') as f:
            os.chmod(key_file, 0600)
            f.write(key.private)
            f.write("\nPAPARIA")

    with open(tmp_ansible_host_file, 'w') as f:
        f.write("[%s]" % tag)

    for machine in assoc_machines:
        ips = [ip for ip in machine.info['public_ips'] if ':' not in ip]
        if not ips:
            break
        ip = ips[0]
        user = machine.info['assoc']['user']
        port = machine.info['assoc']['port']
        key_file = os.path.join(tmp_dir, machine.info['assoc']['key_id'])

        with open(tmp_ansible_host_file, 'a') as f:
            f.write(
                "\n%s\tansible_ssh_host=%s\tansible_ssh_user=%s\tansible_ssh_private_key_file=%s\tansible_ssh_port=%d\n" %
                (machine.name, ip, user, key_file, port)

            )

    return tmp_dir, tmp_ansible_host_file


def parse_output(result, assoc_machines):
    for machine in assoc_machines:
        print "\nFinished in machine: %s" % machine.name
        machine_output = result['contacted'][machine.name]
        failed = machine_output.get("failed", False)

        if failed:
            print "FAILED"
            msg = machine_output.get('msg', None)
            if msg:
                print "Error output: \n%s" % msg
        else:
            stdout = machine_output.get('stdout', None)
            if stdout:
                print "Output: \n%s" % stdout


def ansible_action(args, Runner, Inventory):
    client = authenticate()
    command = args.command
    tag = args.tag

    machines = choose_machines_by_tag(client, tag)
    if not machines:
        print "No machines found with tag: %s" % tag
        sys.exit(0)
    else:
        print "Found tagged machines"

    machines, assoc_keys = update_key_association(client, machines)
    assoc_machines = [machine for machine in machines if machine.info.get('assoc', None)]

    if not assoc_machines:
        print "Could not find machines with associated keys"
        sys.exit(0)

    tmp_dir, tmp_ansible_host_file = init_ansible_tmp_dir(assoc_machines, assoc_keys, tag)

    inventory = Inventory(host_list=tmp_ansible_host_file)

    runner = Runner(module_name='command', module_args=command,  inventory=inventory, host_list=[tag])
    result = runner.run()

    parse_output(result, assoc_machines)
    shutil.rmtree(tmp_dir)
