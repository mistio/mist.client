import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.backends import choose_backend


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

    if args.action == 'list':
        client = authenticate()
        backend = choose_backend(client, args)
        search_term = args.search

        list_images(backend, search_term)