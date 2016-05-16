import os
import sys
import getpass
import ConfigParser
from mistclient import MistClient
from prettytable import PrettyTable


def init_client(mist_uri, email, password, api_token):
    try:
        # TODO regular (username, password) auth
        client = MistClient(mist_uri=mist_uri, email=email, password=password,
                            api_token=api_token)
        # Ensures that GET requests are authenticated
        client.clouds()
        return client
    except Exception as e:
        print e
        sys.exit(1)


def parse_config(renew):
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
    config.set("mist.credentials", "api_token", None)

    # Read configuration file
    if os.path.isfile(config_path):
        config.readfp(open(config_path))
    else:
        print "No config file found at: %s" % config_path

    mist_uri = config.get("mist.io", "mist_uri")
    email = config.get("mist.credentials", "email") or prompt_email()
    password = config.get("mist.credentials", "password") or prompt_password()
    api_token = config.get("mist.credentials", "api_token") or None
    if not api_token or renew:
        # FIXME
        client = MistClient(mist_uri='http://172.17.0.1', email=email, password=password)
    if not os.path.isfile(config_path) or not api_token or renew:
        if client:
            api_token = client.api_token
        prompt_save_config(mist_uri, email, password, api_token, config_path)

    return {
        'mist_uri': mist_uri,
        'email': email,
        'password': password,
        'api_token': api_token
    }


def prompt_save_config(mist_uri, email, password, api_token, config_path):
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
api_token=%s
""" % (mist_uri, email, password, api_token)

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


def authenticate(renew=False):
    config = parse_config(renew)
    return init_client(config["mist_uri"], config["email"],
                       config["password"], config["api_token"])


def user_info():
    client = authenticate()
    user_info = client.user_info()
    user = user_info.user_details()
    plan = user_info.plan_details()
    print "\nUser Details:"
    x = PrettyTable(user.keys())
    x.add_row(user.values())
    print x
    print
    print "Current Plan:"
    x = PrettyTable(plan.keys())
    x.add_row(plan.values())
    print x
    print
