import sys

from netaddr import IPAddress, IPNetwork

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def tunnel_action(args):
    client = authenticate()
    if args.action == 'list-tunnels':
        list_tunnels(client, args.pretty)
    elif args.action == 'add-tunnel':
        add_tunnel(client, args)
        print 'Tunnel %s to %s added successfully' % (args.name, args.cidrs)
    elif args.action == 'edit-tunnel':
        edit_tunnel(client, args)
        print 'Tunnel %s was edited successfully' % args.tunnel_id
    elif args.action == 'delete-tunnel':
        client.delete_tunnel(args.tunnel_id)
        print 'Tunnel %s removed' % args.tunnel_id
    elif args.action == 'tunnel-script':
        get_conf(client, args.tunnel_id)


def list_tunnels(client, pretty):
    tunnels = client.list_tunnels()
    if not tunnels:
        print 'Could not find any VPN Tunnels'
        sys.exit(0)
    if pretty:
        x = PrettyTable(['Name', 'ID', 'CIDRs', 'Description'])
        for tunnel in tunnels:
            description = tunnel.get('description', '-')
            x.add_row([tunnel['name'], tunnel['_id'], tunnel['cidrs'], description])
        print x
    else:
        for tunnel in tunnels:
            description = tunnel.get('description', '-')
            print '%-40s %-40s %-40s %-40s' % (tunnel['name'], tunnel['_id'],
                                               tunnel['cidrs'], description)


def add_tunnel(client, args):
    name = args.name
    cidrs = [cidr.strip(' ') for cidr in str(args.cidrs).split(',')]
    client_addr = args.client_address if args.client_address else ''
    description = args.description

    for network in ['192.168.0.0/16', '172.16.0.0/12', '10.0.0.0/8']:
        for cidr in cidrs:
            if IPNetwork(cidr) in IPNetwork(network):
                break
        else:
            continue
        break
    else:
        while True:
            print 'You are attempting to route a public IP over VPN'
            prompt = raw_input('Are you sure you want to proceed [Y/n]: ')
            if prompt in ['Y', 'y', 'yes']:
                break
            elif prompt in ['N', 'n', 'no']:
                sys.exit(0)

    client.add_tunnel(name=name, cidrs=cidrs, client_addr=client_addr,
                      description=description)


def edit_tunnel(client, args):
    tunnel_id = args.tunnel_id
    name = args.name
    cidrs = [cidr.strip(' ') for cidr in str(args.cidrs).split(',')]
    description = args.description

    client.edit_tunnel(tunnel_id=tunnel_id, name=name, cidrs=cidrs,
                       description=description)


def get_conf(client, tunnel_id):
    tunnels = client.list_tunnels()
    if not tunnels:
        print 'Could not find any VPN Tunnels'
        sys.exit(0)
    for tunnel in tunnels:
        if tunnel['_id'] == tunnel_id:
            script = tunnel['script']
            break
    else:
        print 'The ID provided does not correspond to any VPN Tunnel'
        sys.exit(0)
    print script
