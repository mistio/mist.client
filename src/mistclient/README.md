# mwagger

###Instructions:

    pip install py-dateutil yaml requests

###go to the api folder and run:
    python -m SimpleHTTPServer

###go to the repository folder and import the library:
    from mistclient import MistClient

###Test it:
    client = MistClient(email="dsasd@ds.c", password = "sdasd")
    keys = client.keys()
    clouds = client.clouds()
    rackspace = client.clouds(provider="rackspace")[0]
    rackspace.rename(new_name = "lalal")
