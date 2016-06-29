import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def template_action(args):
    client = authenticate()
    if args.action == 'list-templates':
        list_templates(client, args.pretty)
    elif args.action == 'show-template':
        show_template(client, args.template_id, args.pretty)
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
            x.add_row([template['name'], template['_id'], template['description']])
        print x
    else:
        for template in templates:
            print "%-40s %-40s %-40s" \
                  % (template['name'], template['_id'], template['description'])


def show_template(client, template_id, pretty):
    ret_dict = client.show_template(template_id)
    template = ret_dict['template']
    if not template:
        print 'Template not found'
        sys.exit(0)
    if pretty:
        x = PrettyTable(['Name', 'Description', 'Type', 'Location', 'Deleted'])
        x.add_row([template['name'], template['description'],
                   template['exec_type'], template['location_type'],
                   template['deleted']])
    else:
        print "%-40s %-40s %-40s %-40s %-40s" % (template['name'],
                                                 template['description'],
                                                 template['exec_type'],
                                                 template['location_type'],
                                                 template['deleted'])


def add_template(client, args):
    name = args.name
    if args.template:
        template = args.template
    elif args.template_file:
        if not args.location == 'inline':
            print 'File input is only available for inline templates'
            sys.exit(1)
        with open(args.template_file, 'r') as f:
            template = f.read()
    location_type = args.location
    exec_type = args.type
    entrypoint = args.entrypoint
    description = args.description

    client.add_template(name=name, description=description, template=template,
                        location_type=location_type, exec_type=exec_type,
                        entrypoint=entrypoint)
