import os
import sys
import getpass
import time
import ConfigParser
from mistclient import MistClient
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

    config = ConfigParser.ConfigParser()

    # Set default mist uri
    config.add_section("mist.io")
    config.set("mist.io", "mist_uri", "https://mist.io")

    # Set default credentials
    config.add_section("mist.credentials")
    config.set("mist.credentials", "email", None)
    config.set("mist.credentials", "password", None)

    # Read configuration file
    if os.path.isfile(config_path):
        config.readfp(open(config_path))
    else:
        print "No config file found at: %s" % config_path

    mist_uri = config.get("mist.io", "mist_uri")
    email = config.get("mist.credentials", "email") or prompt_email()
    password = config.get("mist.credentials", "password") or prompt_password()

    if not os.path.isfile(config_path):
        prompt_save_config(mist_uri, email, password, config_path)

    return {
        'mist_uri': mist_uri,
        'email': email,
        'password': password,
    }


def prompt_save_config(mist_uri, email, password, config_path):
    answered = None
    while not answered:
        answer = raw_input("Save config [Y/n]: ")
        if answer in ["y", "Y", "Yes"]:
            answer = True
            answered = True
        elif answer in ["n", "N", "No"]:
            answer = False
            answered = True
        else:
            print "Wrong answer!"

    config_template = """[mist.io]
mist_uri=%s

[mist.credentials]
email=%s
password=%s

""" % (mist_uri, email, password)

    if answer:
        with open(config_path, "w") as f:
            f.write(config_template)
        print "Saved config at %s" % config_path
        return
    else:
        return


def prompt_email():
    return raw_input("Email: ")


def prompt_password():
    return getpass.getpass("Password: ")


def authenticate():
    config = parse_config()
    return init_client(config["mist_uri"], config["email"], config["password"])


def user_info():

    client = authenticate()

    current_plan = client.user_details.get('current_plan')
    user_details = client.user_details.get('user_details')

    print "User Details:"
    x = PrettyTable(user_details.keys())
    x.add_row(user_details.values())
    print x
    print

    print "Current Plan:"
    x = PrettyTable(current_plan.keys())
    expiration = current_plan['expiration']
    current_plan['expiration'] = time.ctime(expiration)
    started = current_plan['started']
    current_plan['started'] = time.ctime(started)
    x.add_row(current_plan.values())
    print x
    print
