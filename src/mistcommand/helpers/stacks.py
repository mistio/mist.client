import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def stack_action(args):
    client = authenticate()
    if args.action == 'list-stacks':
        list_stacks(client, args.pretty)
    elif args.action == 'create-stack':
        create_stack(client, args)
        print "Stack %s based on template %s was successfully created" \
              % (args.stack_name, args.template_id),
        if args.deploy:
            print "and deployed"
    elif args.action == 'delete-stack':
        client.delete_stack(args.stack_id, args.inputs)
        print "Stack %s destroyed" % args.stack_id
    elif args.action == 'run-workflow':
        client.run_workflow(args.stack_id, args.workflow, args.input)
        print "Workflow `%s` was run successfully on stack %s" % (args.worflow,
                                                                  args.stack_id)


def list_stacks(client, pretty):
    stacks = client.get_stacks()
    if not stacks:
        print "No templates found"
        sys.exit(0)
    if pretty:
        x = PrettyTable(["Name", "ID", "Description", "Template", "Deployed"])
        for stack in stacks:
            x.add_row([stack['name'], stack['_id'], stack['description'],
                       stack['template'], stack['deploy']])
        print x
    else:
        for stack in stacks:
            print "%-40s %-40s %-40s %-40s" % (stack['name'], stack['_id'],
                                               stack['description'],
                                               stack['template'])


def create_stack(client, args):
    template_id = args.template_id
    stack_name = args.stack_name
    stack_description = args.stack_description
    deploy = args.deploy
    inputs = args.inputs

    client.create_stack(template_id, stack_name, stack_description,
                        deploy, inputs)
