import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.machines import choose_machine


def list_scripts(client, pretty):
    scripts = client.scripts()
    if not scripts:
        print "No scripts found, create some first"
        sys.exit(0)
    else:
        if pretty:
            x = PrettyTable(['Script Name', 'Script ID', 'Script Description'])
            for script in scripts:
                x.add_row([script.name, script.id, script.description])
            print x
        else:
            for script in scripts:
                print "%-15s  %-35s  %-50s " % (script.name, script.id,
                                                script.description)


def script_action(args):

    client = authenticate()

    if args.action == 'list-scripts':
        pretty = args.pretty
        list_scripts(client, pretty)
    elif args.action == 'add-script':
        if args.script:
            script = args.script
        elif args.script_file:
            if not args.location == 'inline':
                print 'File input is only available for inline scripts'
                sys.exit(1)
            with open(args.script_file, 'r') as f:
                script = f.read()
        kwargs = {
            'name': args.name,
            'description': args.description,
            'script': script,
            'location_type': args.location,
            'exec_type': args.type,
            'entrypoint': args.entrypoint
            # script params ?
        }
        if args.run:
            machine = args.machine_name if args.machine_name else args.machine_id
            if not machine:
                print "Machine name or ID must be specified in order to run " \
                      "the script immediately"
                sys.exit(1)
            machine = choose_machine(client, args)
            machine_id = machine.id
            cloud_id = machine.cloud.id
            # TODO verify script was run successfully
            client.add_and_run_script(cloud_id, machine_id, script_params="",
                                      env=None, su=False, fire_and_forget=True,
                                      **kwargs)
            print "Script %s inserted and ran on machine %s. Check the logs " \
                  "for output" % (args.name, machine.name)
        else:
            client.add_script(**kwargs)
            print "Script %s inserted successfully" % args.name
    elif args.action == 'remove-script':
        resp = client.remove_script(args.id)
        # TODO verify this
        print "Script %s removed" % args.id
    elif args.action == 'run-script':
        machine = args.machine_name if args.machine_name else args.machine_id
        machine = choose_machine(client, args)
        machine_id = machine.id
        cloud_id = machine.cloud.id
        # TODO params
        client.run_script(cloud_id, machine_id, args.id)
        print "Script %s was run. Check the logs for the output" % args.id
