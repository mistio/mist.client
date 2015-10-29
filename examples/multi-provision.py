#!/usr/bin/env python
"""
multi-provision is a Python script which allows you to provision multiple
virtual machines on any provider supported by mist.io

This script has the following capabilities:
    * Deploy a specified amount of virtual machines
    * Print out information of the main network interface (mac and ip)
    * Run a post-processing script on each of the machines

--- Requirements ---
pip install -U mist

--- Usage ---
Run 'multi-provision.py -h' for an overview

--- Author ---
Dimitris Moraits

--- License ---
MIT
"""

import argparse
import getpass
import logging
import sys
import json

from mistclient import MistClient
from mistcommand.helpers.login import parse_config


def get_args():
    """
    Supports the command-line arguments listed below.
    """

    parser = argparse.ArgumentParser(
        description="Provision multiple VM's through mist.io. You can get "
        "information returned with the name of the virtual machine created "
        "and its main mac and ip address in IPv4 format. A post-script can be "
        "specified for post-processing.")
    parser.add_argument('-b', '--basename', nargs=1, required=True,
                        help='Basename of the newly deployed VMs',
                        dest='basename', type=str)
    parser.add_argument('-d', '--debug', required=False,
                        help='Enable debug output', dest='debug',
                        action='store_true')
    parser.add_argument('-i', '--print-ips', required=False,
                        help='Enable IP output', dest='ips',
                        action='store_true')
    parser.add_argument('-m', '--print-macs', required=False,
                        help='Enable MAC output', dest='macs',
                        action='store_true')
    parser.add_argument('-l', '--log-file', nargs=1, required=False,
                        help='File to log to (default = stdout)',
                        dest='logfile', type=str)
    parser.add_argument('-n', '--number', nargs=1, required=False,
                        help='Amount of VMs to deploy (default = 1)',
                        dest='quantity', type=int, default=[1])
    parser.add_argument('-M', '--monitoring', required=False,
                        help='Enable monitoring on the virtual machines',
                        dest='monitoring', action='store_true')
    parser.add_argument('-B', '--backend-name', required=False,
                        help='The name of the backend to use for provisioning.'
                        ' Defaults to the first available backend',
                        dest='backend_name', type=str)
    parser.add_argument('-I', '--image-id', required=True,
                        help='The image to deploy', dest='image_id')
    parser.add_argument('-S', '--size-id', required=True,
                        help='The id of the size/flavor to use',
                        dest='size_id')
    parser.add_argument('-N', '--networks', required=False, nargs='+',
                        help='The ids of the networks to assign to the VMs',
                        dest='networks')
    parser.add_argument('-s', '--post-script', nargs=1, required=False,
                        help='Script to be called after each VM is created and'
                        ' booted.', dest='post_script', type=str)
    parser.add_argument('-P', '--script-params', nargs=1, required=False,
                        help='Script to be called after each VM is created and'
                        ' booted.', dest='script_params', type=str)
    parser.add_argument('-H', '--host', required=False,
                        help='mist.io instance to connect to', dest='host',
                        type=str, default='https://mist.io')
    parser.add_argument('-u', '--user', nargs=1, required=False,
                        help='email registered to mist.io', dest='username',
                        type=str)
    parser.add_argument('-p', '--password', nargs=1, required=False,
                        help='The password with which to connect to the host. '
                        'If not specified, the user is prompted at runtime for'
                        ' a password', dest='password', type=str)
    parser.add_argument('-v', '--verbose', required=False,
                        help='Enable verbose output', dest='verbose',
                        action='store_true')
    parser.add_argument('-w', '--wait-max', nargs=1, required=False,
                        help='Maximum amount of seconds to wait when gathering'
                        ' information (default = 600)', dest='maxwait',
                        type=int, default=[600])
    parser.add_argument('-f', '--associate-floating-ip', required=False, action='store_true',
                        help='Auto-associates floating ips to vms in Openstack backens',
                        dest='associate_floating_ip',)
    args = parser.parse_args()
    return args


def main():
    # Handling arguments
    args = get_args()

    backend_name = None
    if args.backend_name:
        backend_name = args.backend_name

    basename = args.basename[0]
    image_id = args.image_id
    size_id = args.size_id

    monitoring = args.monitoring

    quantity = args.quantity[0]

    print_ips = args.ips
    print_macs = args.macs

    associate_floating_ip = args.associate_floating_ip

    host = args.host.rstrip('/')

    username = None
    if args.username:
        username = args.username[0]

    password = None
    if args.password:
        password = args.password[0]

    log_file = None
    if args.logfile:
        log_file = args.logfile[0]

    post_script = None
    if args.post_script:
        post_script = args.post_script[0]
    script_params = ''
    if args.script_params:
        script_params = args.script_params[0]
    if args.networks:
        networks = args.networks

    debug = args.debug
    verbose = args.verbose
    maxwait = args.maxwait[0]

    # Logging settings
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    if log_file:
        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=log_level)
    else:
        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=log_level)
    logger = logging.getLogger(__name__)

    # Getting user password
    if username and password is None:
        logger.debug('No command line password received, requesting password '
                     'from user')
        password = getpass.getpass(prompt='Enter mist.io password for user %s:'
                                   % (username))

    try:
        client = None
        try:
            logger.info('Connecting to mist.io with username %s' % (username))
            if username:
                client = MistClient(email=username, password=password,
                                    mist_uri=host, verify=False)
            else:
                credentials = parse_config()
                client = MistClient(email=credentials['email'],
                                    password=credentials['password'],
                                    mist_uri=credentials['mist_uri'])
        except IOError, e:
            pass

        if not client:
            logger.error('Could not connect to mist.io with user %s and '
                         'specified password' % (username))
            return 1

        # Get the requested or first backend
        if backend_name:
            backends = client.backends(name=backend_name)
        else:
            backends = client.backends()

        if not backends:
            logger.critical('Backend unavailable')
            return 1
        else:
            backend = backends[0]

        # Create a new ssh keypair for this deployment
        private = client.generate_key()
        try:
            client.add_key(key_name=basename, private=private)
        except:
            logger.warn('Key %s already exists' % basename)

        res = backend.create_machine(name=basename,
                                     key=client.keys(search=basename)[0],
                                     image_id=image_id,
                                     location_id=backend.locations[0]['id'],
                                     size_id=size_id,
                                     networks=args.networks,
                                     async=True,
                                     fire_and_forget=False,
                                     quantity=quantity,
                                     monitoring=monitoring,
                                     verbose=True,
                                     timeout=maxwait,
                                     associate_floating_ip=associate_floating_ip
                                     )

        if print_ips or post_script:
            try:
                logger.info('Updating VM list from backend')
                backend.update_machines()
            except:  # Retry in case of network glitch
                logger.warn('Backend unavailable. Retrying')
                backend.update_machines()

            probes = [p for p in res['logs']
                      if p['action'] == 'probe' and not p['error']]
            for p in probes:
                try:
                    machine = backend.machines(p['machine_id'])[0]
                except:
                    machine = None

                print '----------'
                if machine:
                    print 'Machine:', machine.name
                    if print_ips:
                        print 'Public ip addresses:'
                        for i in machine.info.get('public_ips', []):
                            print " - ", i
                        print 'Private ip addresses:'
                        for i in machine.info.get('private_ips'):
                            print " - ", i
                else:
                    print 'Machine:', p['machine_id']

                if print_macs:
                    print 'MACS:', json.dumps(p.get('result', {}).get('macs'))

                if post_script:
                    job = client.run_script(backend.id, p['machine_id'],
                                            post_script,
                                            script_params=script_params,
                                            fire_and_forget=True)
                    if job.get('job_id'):
                        print 'Post deployment script queued: %s/jobs/%s' % \
                              (host, job.get('job_id'))

            print '----------'

    except Exception, e:
        logger.critical('Caught exception: %s' % str(e))
        return 1

    logger.info('Finished all tasks')
    return 0

# Start program
if __name__ == "__main__":
    main()
