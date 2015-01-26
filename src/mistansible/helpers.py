import os
import ConfigParser
from mistclient import MistClient


def authenticate(module):
    home_path = os.getenv("HOME")
    config_path = os.path.join(home_path, '.mist')
    config = ConfigParser.ConfigParser()

    mist_uri = module.params.get('mist_uri')
    mist_email = module.params.get('mist_email')
    mist_password = module.params.get('mist_password')

    # Set mist uri
    config.add_section("mist.io")
    if not mist_uri:
        config.set("mist.io", "mist_uri", "https://mist.io")
    else:
        config.set("mist.io", "mist_uri", mist_uri)

    # Set default credentials
    config.add_section("mist.credentials")
    config.set("mist.credentials", "email", None)
    config.set("mist.credentials", "password", None)

    # Read configuration file
    if os.path.isfile(config_path):
            config.readfp(open(config_path))

    mist_uri = config.get("mist.io", "mist_uri")
    if not mist_email:
        mist_email = config.get("mist.credentials", "email") or ""

    if not mist_password:
        mist_password = config.get("mist.credentials", "password") or ""

    return init_client(mist_uri, mist_email, mist_password)


def init_client(mist_uri="https://mist.io", email=None, password=None):
    client = MistClient(mist_uri, email, password)
    return client