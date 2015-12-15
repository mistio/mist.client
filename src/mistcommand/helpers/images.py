import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate
from mistcommand.helpers.clouds import return_cloud


def list_images(cloud, search_term, pretty):
    if not search_term:
        images = []
        for image in cloud.images:
            if image['star']:
                images.append(image)
    elif search_term == "all":
        images = cloud.images
    else:
        images = cloud.search_image(search_term)

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
        cloud = return_cloud(client, args)
        search_term = args.search
        pretty = args.pretty

        list_images(cloud, search_term, pretty)