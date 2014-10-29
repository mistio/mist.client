import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def list_images(backend, search_term):
    if not search_term:
        images = []
        for image in backend.images:
            if image['star']:
                images.append(image)
    elif search_term == "all":
        images = backend.images
    else:
        images = backend.search_image(search_term)

    x = PrettyTable(["Name", "ID"])
    for image in images:
        x.add_row([image['name'], image['id']])

    print x


def image_action(args):

    client = authenticate()

    backend_value = args.backend
    search_term = args.search

    if args.action in ["list", "ls"] and args.target == "images":
        if not backend_value:
            print "You have to provide either backend name or backend id"
            sys.exit(1)
        else:
            backend = client.search_backend(backend_value)

        list_images(backend, search_term)