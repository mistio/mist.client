import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate

def list_scripts(client, pretty):
    scripts = client.scripts()


    if not scripts:
        print "No scripts found, create some first"
        sys.exit(0)

    else:
        print 'Script Name - Script ID - Script Description'
        for script in scripts:
            print "%s  %s  %s " % (script.name, script.id, script.description)

def script_action(args):

    client = authenticate()

    if args.action == 'list-scripts':
        pretty = args.pretty
        list_scripts(client, pretty)

