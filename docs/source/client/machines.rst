Machines
********

Before you can provision a machine, you have to know some data that are necessary for the creation of a machine. Every
backend has different OS Images, locations, machine sizes. You can list all the available options after you have chosen
a backend::

    backend = client.backends(search="NephoScale")

Images
======
You can list all available OS Images in a backend::

    backend.images

This will return a list of all available images. From the desired image you will need the image's id in order to create
a machine with that image::

    [{u'extra': {u'architecture': u'x86',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/3/'},
      u'id': u'3',
      u'name': u'Linux CentOS 5.5 32-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86_64',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/5/'},
      u'id': u'5',
      u'name': u'Linux CentOS 5.5 64-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/23/'},
      u'id': u'23',
      u'name': u'Linux Debian Server 5.05 32-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/43/'},
      u'id': u'43',
      u'name': u'Linux Ubuntu Server 10.04 LTS 32-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/45/'},
      u'id': u'45',
      u'name': u'Linux CentOS 5.7 32-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86_64',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/49/'},
      u'id': u'49',
      u'name': u'Linux Ubuntu Server 10.04 LTS 64-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86_64',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/51/'},
      u'id': u'51',
      u'name': u'Linux Debian Server 6.0.3 64-bit',
      u'star': True},
     {u'extra': {u'architecture': u'x86_64',
       u'billable_type': None,
       u'cores': None,
       u'disks': None,
       u'pcpus': None,
       u'storage': None,
       u'uri': u'https://api.nephoscale.com/image/server/55/'},
      u'id': u'55',
      u'name': u'Linux Debian 5.0.9 64-bit',
      u'star': True}]

    image_id = backend.images[0]['id']

You also have the option to search for an image. Especially in EC2 backends, the result of the search will include
community and public images::

    backend.search_image("Debian")

Sizes
=====
To list available machine sizes for the chosen backend::

    backend.sizes

From the list of all available sizes, you'll also need the id of the desired size::

    [{u'bandwidth': None,
      u'disk': 25,
      u'driver': u'NephoScale',
      u'id': u'219',
      u'name': u'CS05-SSD - 0.5GB, 1Core, 25GB, 10 Gbps',
      u'price': None,
      u'ram': 512},
     {u'bandwidth': None,
      u'disk': 25,
      u'driver': u'NephoScale',
      u'id': u'221',
      u'name': u'CS1-SSD - 1GB, 1Core, 25GB, 10 Gbps',
      u'price': None,
      u'ram': 1024},
      ...

    size_id = backend.sizes[0]['id']

Locations
=========
Some backends have different locations for you to provision a machine to. You can list them::

    backend.locations

From the list of available locations, you'll need the id of the desired location::

    [{u'country': u'US', u'id': u'86945', u'name': u'SJC-1'},
     {u'country': u'US', u'id': u'87729', u'name': u'RIC-1'}]

    location_id = backend.locations[0]

Create machines
===============
In order to create a machine you basically need to have chosen a backend, a key, image_id, location_id, size_id and a
name for the machine::

    backend.create_machine(name="production.server", key=key, image_id=image_id, location_id=location_id, size_id=size_id)

In some backends some extra information is needed. You can see ``mistclient.model.Backend.create_machine`` method for more details.

Machine actions
===============
You can see a list of all your created machines for a given backend::

    client.machines()

Or for a specific backend::

    backend.machines()


You can choose one::

    machine = client.machines(search="dev")[0]
    machine = client.machines(name="dbserver1")[0]


Machines support actions like::

    machine.reboot()
    machine.start()
    machine.stop()
    machine.destroy()

After creating a machine, the machine may take some time to be up and running. You can see that by using ``machine.probe()``.
Machine probe, if successful will show that the machine is up and running and that the key association was successful. It will
also return some useful information about the machine like the machine's uptime etc.

In case you want, you can associate another ssh-key to the machine, provided you have uploaded that key to mist.io service::

    machine.associate_key(key_id, host="187.23.43.98")

The host of the machine can be found in the machine.info['public_ips'] list. You can also provide two more parameters.
``ssh_user`` and ``ssh_port``.
