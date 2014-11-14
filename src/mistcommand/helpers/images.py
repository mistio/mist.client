import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import return_backend


def list_images(backend, search_term, pretty):
    if not search_term:
        images = []
        for image in backend.images:
            if image['star']:
                images.append(image)
    elif search_term == "all":
        images = backend.images
    else:
        images = backend.search_image(search_term)

    if pretty:
        x = PrettyTable(["Name", "ID"])
        for image in images:
            x.add_row([image['name'], image['id']])

        print x
    else:
        for image in images:
            print "%-40s %-40s" % (image['name'], image['id'])


def image_action(args):

    if args.action == 'list-images':
        client = authenticate()
        backend = return_backend(client, args)
        search_term = args.search
        pretty = args.pretty

        list_images(backend, search_term, pretty)