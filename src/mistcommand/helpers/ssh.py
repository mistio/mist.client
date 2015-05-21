import socket
import sys
import tempfile
import os
from paramiko.py3compat import u
from mistcommand.helpers.login import authenticate

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass


def find_key_assoc(client, machine):
    keys = client.keys()
    connection_info = {}

    for key in keys:
        assoc_machines = key.info['machines']
        for assoc_machine in assoc_machines:
            id = assoc_machine[1]
            if machine.id == id:
                connection_info['user'] = assoc_machine[3]
                connection_info['port'] = assoc_machine[-1]
                found_key = key
                break

    return found_key, connection_info


def init_client(hostname, port, user, key_file):
    import paramiko
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "Connecting to: %s:%s" % (hostname, str(port))
    print "User: %s" % user
    print "Keyfile: %s" % key_file
    print

    client.connect(hostname, port, user, key_filename=key_file)
    chan = client.invoke_shell()
    print repr(client.get_transport())

    print '*** Here we go!'

    interactive_shell(chan)
    chan.close()
    client.close()


def temp_keyfile(key):
    tmp_dir = tempfile.mkdtemp()
    key_file = os.path.join(tmp_dir, key.id)
    with open(key_file, 'w') as f:
        os.chmod(key_file, 0600)
        f.write(key.private)

    return key_file


def ssh_action(args):
    client = authenticate()

    print "Searching machine..."
    print
    machines = client.machines(name=args.machine)
    if not machines:
        print "Could not find machine: %s" % args.machine
        sys.exit(1)
    else:
        print "Found machine"
        print
        machine = machines[0]

    probed = machine.probe()
    if not probed:
        print "Machine is not probed (maybe still provisioning or no key is associated)."
        sys.exit(0)
    else:
        print "Machine is probed. Gathering info for ssh connection"
        print

    key, connection_info = find_key_assoc(client, machine)

    if key and connection_info:
        print "Found info"

    key_path = temp_keyfile(key)

    machine_ip = machine.info['public_ips'][0]

    init_client(hostname=machine_ip, port=int(connection_info['port']), user=connection_info['user'],
                key_file=key_path)
