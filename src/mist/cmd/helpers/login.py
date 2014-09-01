import os
import sys
import getpass
import time
import ConfigParser
from mist.client import MistClient
from prettytable import PrettyTable


def init_client(mist_uri, email, password):
    try:
        client = MistClient(mist_uri=mist_uri, email=email, password=password)

        #Ensures that GET requests are autheticated
        client.backends
        return client
    except Exception as e:
        print e
        sys.exit(1)


def parse_config():
    home_path = os.getenv("HOME")
    config_path = os.path.join(home_path, ".mist")

    if not os.path.isfile(config_path):
        print "No config file found at: %s" % config_path
        return None

    config = ConfigParser.ConfigParser()
    config.readfp(open(config_path))

    mist_uri = config.get("mist.io", "mist_uri")
    email = config.get("mist.credentials", "email")
    password = config.get("mist.credentials", "password")

    return {
        'mist_uri': mist_uri,
        'email': email,
        'password': password
    }


def prompt_login():
    email = raw_input("Email: ")
    password = getpass.getpass("Password: ")
    print

    return email, password


def user_info():
    result = parse_config()
    if not result:
        mist_uri = "https://mist.io"
        email, password = prompt_login()
    else:
        mist_uri = result['mist_uri']
        email = result['email']
        password = result['password']

    client = init_client(mist_uri, email, password)
    current_plan = client.user_details.get('current_plan')
    user_details = client.user_details.get('user_details')

    print "User Details:"
    x = PrettyTable(user_details.keys())
    x.add_row(user_details.values())
    print x
    print

    print "Current Plan"
    x = PrettyTable(current_plan.keys())
    expiration = current_plan['expiration']
    current_plan['expiration'] = time.ctime(expiration)
    x.add_row(current_plan.values())
    print x
    print