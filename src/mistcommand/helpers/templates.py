import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def template_action(args):
    client = authenticate()
    if args.action == 'list-templates':
        list_templates(client, args.pretty)
    elif args.action == 'add-template':
        add_template(client, args)
        print "Template %s added successfully" % args.name
    elif args.action == 'delete-template':
        client.delete_template(args.template_id)
        print "Template %s removed" % args.template_id


def list_templates(client, pretty):
    templates = client.get_templates()
    if not templates:
        print "No templates found"
        sys.exit(0)
    if pretty:
        x = PrettyTable(["Name", "ID", "Description"])
        for template in templates:
            x.add_row([template['name'], template['id'], template['description']])
        print x
    else:
        for template in templates:
            print "%-40s %-40s %-40s" \
                  % (template['name'], template['id'], template['description'])


def add_template(client, args):
    name = args.name
    template = args.template
    location_type = args.location
    exec_type = args.type
    entrypoint = args.entrypoint
    description = args.description

    client.add_template(name=name, description=description, template=template,
                        location_type=location_type, exec_type=exec_type,
                        entrypoint=entrypoint)
