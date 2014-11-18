Quickstart  Guide
*****************

In this quickstart guide we'll see how to provision and manage servers on an Openstack backend.

``pip install mist``

After installing mist::

    from mistclient import MistClient
    client = MistClient(email="demo@mist.io", password="supersecret")

We have a stack of 4 machines to provision::

    machines = [
    'dbserver1',
    'dbserver2',
    'haproxy',
    'webserver'
    ]

We add our Openstack backend::

    client.add_backend(title="Openstack", proviser="openstack", key="admin', secret="admin_pass", apiurl="http://10.0.0.1:5000", tenant_name="admin")

We then provision those machines in this newly added Openstack backend, using a auto-generated key::

    private = client.generate_key()
    key = client.add_key(key_name="MyKey", private=private)
    backend = client.backends(search="Openstack")[0]

    for machine in machines:
        backend.create_machine(name=machine, key=key, image_id="a098798798-9809808-098098", size_id="2", location_id="1")

We then tag the machines with the ``dev`` tag::

    for machine_name in machines:
        machine = client.machines(name=machine_name)
        machine.tag("dev")

We will now use the ``mist`` command line tool to manage those servers. Use the ``mist run`` option to run a command
accross tagged servers::

    mist run --command "apt-get update -y" --tag dev

