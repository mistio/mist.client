Backends
********

A backend can be an IaaS cloud, a Docker host, or any single server.

Supported Providers
===================
Mist.io supports a big list of providers including EC2, Rackspace, SoftLayer, Digital Ocean, Nephoscale, Openstack,
Docker, HP Cloud and any single server.

In order to see the list of all supported providers::

    client.supported_providers

The result will look like this::

    [{u'provider': u'bare_metal', u'title': u'Bare Metal Server'},
    {u'provider': u'ec2_ap_northeast', u'title': u'EC2 AP NORTHEAST'},
    {u'provider': u'ec2_ap_southeast', u'title': u'EC2 AP SOUTHEAST'},
    {u'provider': u'ec2_ap_southeast_2', u'title': u'EC2 AP Sydney'},
    {u'provider': u'ec2_eu_west', u'title': u'EC2 EU Ireland'},
    {u'provider': u'ec2_sa_east', u'title': u'EC2 SA EAST'},
    {u'provider': u'ec2_us_east', u'title': u'EC2 US EAST'},
    {u'provider': u'ec2_us_west', u'title': u'EC2 US WEST'},
    {u'provider': u'ec2_us_west_oregon', u'title': u'EC2 US WEST OREGON'},
    {u'provider': u'gce', u'title': u'Google Compute Engine'},
    {u'provider': u'nephoscale', u'title': u'NephoScale'},
    {u'provider': u'digitalocean', u'title': u'DigitalOcean'},
    {u'provider': u'linode', u'title': u'Linode'},
    {u'provider': u'openstack', u'title': u'OpenStack'},
    {u'provider': u'rackspace:dfw', u'title': u'Rackspace DFW'},
    {u'provider': u'rackspace:ord', u'title': u'Rackspace ORD'},
    {u'provider': u'rackspace:iad', u'title': u'Rackspace IAD'},
    {u'provider': u'rackspace:lon', u'title': u'Rackspace LON'},
    {u'provider': u'rackspace:syd', u'title': u'Rackspace AU'},
    {u'provider': u'rackspace:hkg', u'title': u'Rackspace HKG'},
    {u'provider': u'rackspace_first_gen:us', u'title': u'Rackspace US (OLD)'},
    {u'provider': u'rackspace_first_gen:uk', u'title': u'Rackspace UK (OLD)'},
    {u'provider': u'softlayer', u'title': u'SoftLayer'},
    {u'provider': u'hpcloud:region-a.geo-1',
    u'title': u'HP Helion Cloud - US West'},
    {u'provider': u'hpcloud:region-b.geo-1',
    u'title': u'HP Helion Cloud - US East'},
    {u'provider': u'docker', u'title': u'Docker'}]

Add Backend
===========
Before anything you must add your Backends to the mist.io service. By doing that you'll be able to handle all your
machines from the mist.io service or the service's API.

In order to add a backend, you'll need the ``provider`` information from the supported providers you listed before. For
example to add a "Rackspace LON" backend::

    client.add_backend(provider="rackspace:lon", title="My Rack London", key="rack_username", secret="rack_api_secret")



See also ``mist.client.add_backend`` method for detailed information about the different params for each backend.

After adding a new backend, mist.backends are automatically updated.

Backend actions
==============
You can see all of your added backends::

    client.backends

This will return a dict like this::

    {u'2zMXgapqqaw9bSNUzSmuygFLy6Kp': Backend => Rackspace ORD, rackspace, 2zMXgapqqaw9bSNUzSmuygFLy6Kp,
     u'36vp27TVyUCarDNNcta1Knsqcr8Z': Backend => Rackspace AU, rackspace, 36vp27TVyUCarDNNcta1Knsqcr8Z,
     u'3aJhBzUtAMnCUmpEHKJsqLdm1Z9p': Backend => DigitalOcean, digitalocean, 3aJhBzUtAMnCUmpEHKJsqLdm1Z9p,
     u'B3rbEA6bteaqMWJ4obVbgbqrXWf': Backend => Docker, docker, B3rbEA6bteaqMWJ4obVbgbqrXWf,
     u'W16qxKErSArH9DSNJyxXU81n35w': Backend => NephoScale, nephoscale, W16qxKErSArH9DSNJyxXU81n35w}

You can choose a backend::

    backend = client.backends['2zMXgapqqaw9bSNUzSmuygFLy6Kp']

You can also choose a backend by providing either the backend's name or id::

    backend = client.backend_from_id("2zMXgapqqaw9bSNUzSmuygFLy6Kp")
    backend = client.backend_from_name("DigitalOcean")

You can also use the overloaded function ``client.search_backend("search_term")`` by providing either an id
or a name and it will return the first backend with that has either an id or name that matches the given
parameter.

Your new backend object has a lot of attributes and methods::

    backend.id
    backend.info
    backend.images
    ...

See ``mist.client.model.Backend`` class for detailed information.

You have the option to rename a backend::

    backend.rename("newName"


Finally, you can delete a backend::

    backend.delete()

