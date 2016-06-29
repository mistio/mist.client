import sys

from netaddr import IPAddress, IPNetwork

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def tunnel_action(args):
    client = authenticate()
    if args.action == 'list-tunnels':
        list_tunnels(client, args.pretty)
    elif args.action == 'add-tunnel':
        tunnel = add_tunnel(client, args)
        print '\nTunnel <%s> to %s added successfully\n' % (args.name, args.cidrs)
        print 'Now, copy-paste and run the configuration script on your VPN ' \
              'client in order to complete the VPN tunnel\'s establishment\n'
        print '='*50 + '\n'
        get_conf(client, tunnel['_id'])
        print '='*50 + '\n'
        print 'Or, you can simply run the following `curl` command directly ' \
              'in your VPN client\'s shell:\n'
        get_cmd(client, tunnel['_id'])
    elif args.action == 'edit-tunnel':
        edit_tunnel(client, args)
        print 'Tunnel %s was edited successfully' % args.tunnel
    elif args.action == 'delete-tunnel':
        client.delete_tunnel(args.tunnel)
        print 'Tunnel %s removed' % args.tunnel
    elif args.action == 'tunnel-script':
        get_conf(client, args.tunnel)
    elif args.action == 'tunnel-command':
        get_cmd(client, args.tunnel)


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
    cidrs = args.cidrs
    excluded_cidrs = args.exclude_cidrs if args.exclude_cidrs else []
    description = args.description

    for cidr in cidrs:
        for network in ['192.168.0.0/16', '172.16.0.0/12', '10.0.0.0/8']:
            if IPNetwork(cidr) in IPNetwork(network):
                break
        else:
            while True:
                print 'You are attempting to route a public IP over VPN'
                prompt = raw_input('Are you sure you want to proceed [Y/n]: ')
                if prompt in ['Y', 'y', 'yes']:
                    break
                elif prompt in ['N', 'n', 'no']:
                    sys.exit(0)
            break

    return client.add_tunnel(name=name, cidrs=cidrs,
                             excluded_cidrs=excluded_cidrs,
                             description=description)


def edit_tunnel(client, args):
    tunnel_id = args.tunnel
    name = args.name
    cidrs = args.cidrs
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


def get_cmd(client, tunnel_id):
    print client.tunnel_command(tunnel_id)
