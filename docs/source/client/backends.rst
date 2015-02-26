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

    [{u'provider': u'bare_metal', u'regions': [], u'title': u'Other Server'},
     {u'provider': u'azure', u'regions': [], u'title': u'Azure'},
     {u'provider': u'ec2',
      u'regions': [{u'id': u'ec2_ap_northeast', u'location': u'Tokyo'},
       {u'id': u'ec2_ap_southeast', u'location': u'Singapore'},
       {u'id': u'ec2_ap_southeast_2', u'location': u'Sydney'},
       {u'id': u'ec2_eu_west', u'location': u'Ireland'},
       {u'id': u'ec2_sa_east', u'location': u'Sao Paulo'},
       {u'id': u'ec2_us_east', u'location': u'N. Virginia'},
       {u'id': u'ec2_us_west', u'location': u'N. California'},
       {u'id': u'ec2_us_west_oregon', u'location': u'Oregon'}],
      u'title': u'EC2'},
     {u'provider': u'gce', u'regions': [], u'title': u'Google Compute Engine'},
     {u'provider': u'nephoscale', u'regions': [], u'title': u'NephoScale'},
     {u'provider': u'digitalocean', u'regions': [], u'title': u'DigitalOcean'},
     {u'provider': u'linode', u'regions': [], u'title': u'Linode'},
     {u'provider': u'openstack', u'regions': [], u'title': u'OpenStack'},
     {u'provider': u'rackspace',
      u'regions': [{u'id': u'dfw', u'location': u'Dallas'},
       {u'id': u'ord', u'location': u'Chicago'},
       {u'id': u'iad', u'location': u'N. Virginia'},
       {u'id': u'lon', u'location': u'London'},
       {u'id': u'syd', u'location': u'Sydney'},
       {u'id': u'hkg', u'location': u'Hong Kong'},
       {u'id': u'rackspace_first_gen:us', u'location': u'US-First Gen'},
       {u'id': u'rackspace_first_gen:uk', u'location': u'UK-First Gen'}],
      u'title': u'Rackspace'},
     {u'provider': u'softlayer', u'regions': [], u'title': u'SoftLayer'},
     {u'provider': u'hpcloud',
      u'regions': [{u'id': u'region-a.geo-1', u'location': u'US West'},
       {u'id': u'region-b.geo-1', u'location': u'US East'}],
      u'title': u'HP Helion Cloud'},
     {u'provider': u'docker', u'regions': [], u'title': u'Docker'},
     {u'provider': u'vcloud', u'regions': [], u'title': u'VMware vCloud'},
     {u'provider': u'indonesian_vcloud',
      u'regions': [],
      u'title': u'Indonesian Cloud'},
     {u'provider': u'libvirt', u'regions': [], u'title': u'KVM (via libvirt)'}]

Add Backend
===========
Before anything you must add your Backends to the mist.io service. By doing that you'll be able to handle all your
machines from the mist.io service or the service's API.

In order to add a backend, you'll need the ``provider`` information from the supported providers you listed before. For
example to add a "Rackspace LON" backend::

    client.add_backend(provider="rackspace", title="My Rack London", region="lon", username="rack_username", api_key="rack_api_secret")



See also ``mist.client.add_backend`` method for detailed information about the different params for each backend.

After adding a new backend, mist.backends are automatically updated.

Backend actions
===============
You can see all of your added backends::

    client.backends()

This will return a list of all your added backends::

    [Backend => EC2 AP NORTHEAST, ec2_ap_northeast, D1g9abwqGUmQuZKGGBMfCgw8AUQ,
     Backend => openstackaf0.mist.io, bare_metal, 2Mn2ZnCoXhK3ywqzGn1fzWVmSSe6,
     Backend => Icehouse, openstack, 4ukW6Juooqa8bTu2YgM4mE8RAsk7,
     Backend => EC2 AP Sydney, ec2_ap_southeast_2, 25ykPERh5D17DyoeKsCgw35DLmvw,
     Backend => Openstack Juno, openstack, 2u5yKqXmDiZ7BHCk1u17FFcmFS2m,
     Backend => HP Helion Cloud, hpcloud, 3WwgPBXETjdeMEbM5fUCACSvedGT,
     Backend => Google Compute Engine, gce, g6T3HYae2ZMcHfHyFGKVtMG6PZU,
     Backend => Docker, docker, B3rbEA6bteaqMWJ4obVbgbqrXWf,
     Backend => openstackdfe.mist.io, bare_metal, XMdRN2u3NVASMm14BuHo4HJnS15]


You can also choose a backend by providing either the backend's name or id::

    backend = client.backends(id="XMdRN2u3NVASMm14BuHo4HJnS15")[0]
    backend = client.backends(name="Docker")[0]

You can also search in all the backends' ids and names::

    backend = client.backends(search="OpenStack")[0]

Your new backend object has a lot of attributes and methods::

    backend.id
    backend.info
    backend.images
    ...

See ``mistclient.model.Backend`` class for detailed information.

You have the option to rename a backend::

    backend.rename("newName")


Finally, you can delete a backend::

    backend.delete()

