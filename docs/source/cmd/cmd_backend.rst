mist backends
*************

With mist you can handle multiple machines on multiple providers from one interface, the mist.io service.
In order to do so, the very first thing to do when using mist.io is to ensure that you have added your backends.
After doing that you'll be able to provision, monitor and in general handle all your machines on all
those providers.

Supported Providers
===================
Before you add a new backend, you'll find it useful to see a list of all the providers that mist.io supports::

    mist list-providers

Output::

    Bare Metal Server              bare_metal
    Azure                          azure
    EC2 AP NORTHEAST               ec2_ap_northeast
    EC2 AP SOUTHEAST               ec2_ap_southeast
    EC2 AP Sydney                  ec2_ap_southeast_2
    EC2 EU Ireland                 ec2_eu_west
    EC2 SA EAST                    ec2_sa_east
    EC2 US EAST                    ec2_us_east
    EC2 US WEST                    ec2_us_west
    EC2 US WEST OREGON             ec2_us_west_oregon
    Google Compute Engine          gce
    NephoScale                     nephoscale
    DigitalOcean                   digitalocean
    Linode                         linode
    OpenStack                      openstack
    Rackspace DFW                  rackspace:dfw
    Rackspace ORD                  rackspace:ord
    Rackspace IAD                  rackspace:iad
    Rackspace LON                  rackspace:lon
    Rackspace AU                   rackspace:syd
    Rackspace HKG                  rackspace:hkg
    Rackspace US (OLD)             rackspace_first_gen:us
    Rackspace UK (OLD)             rackspace_first_gen:uk
    SoftLayer                      softlayer
    HP Helion Cloud - US West      hpcloud:region-a.geo-1
    HP Helion Cloud - US East      hpcloud:region-b.geo-1
    Docker                         docker

.. Note:: With every *list* action, you can have the output in a more *pretty* format by providing the ``--pretty`` flag.

For example, ``mist list-providers --pretty`` will return this output::

    +---------------------------+------------------------+
    |           Title           |      Provider ID       |
    +---------------------------+------------------------+
    |     Bare Metal Server     |       bare_metal       |
    |           Azure           |         azure          |
    |      EC2 AP NORTHEAST     |    ec2_ap_northeast    |
    |      EC2 AP SOUTHEAST     |    ec2_ap_southeast    |
    |       EC2 AP Sydney       |   ec2_ap_southeast_2   |
    |       EC2 EU Ireland      |      ec2_eu_west       |
    |        EC2 SA EAST        |      ec2_sa_east       |
    |        EC2 US EAST        |      ec2_us_east       |
    |        EC2 US WEST        |      ec2_us_west       |
    |     EC2 US WEST OREGON    |   ec2_us_west_oregon   |
    |   Google Compute Engine   |          gce           |
    |         NephoScale        |       nephoscale       |
    |        DigitalOcean       |      digitalocean      |
    |           Linode          |         linode         |
    |         OpenStack         |       openstack        |
    |       Rackspace DFW       |     rackspace:dfw      |
    |       Rackspace ORD       |     rackspace:ord      |
    |       Rackspace IAD       |     rackspace:iad      |
    |       Rackspace LON       |     rackspace:lon      |
    |        Rackspace AU       |     rackspace:syd      |
    |       Rackspace HKG       |     rackspace:hkg      |
    |     Rackspace US (OLD)    | rackspace_first_gen:us |
    |     Rackspace UK (OLD)    | rackspace_first_gen:uk |
    |         SoftLayer         |       softlayer        |
    | HP Helion Cloud - US West | hpcloud:region-a.geo-1 |
    | HP Helion Cloud - US East | hpcloud:region-b.geo-1 |
    |           Docker          |         docker         |
    +---------------------------+------------------------+

From here on you'll need your desired provider's id in order to use it when adding a new backend.

Backend Actions
===============
To add a new backend you'll need at least the provider's id, a name for the backend, an apikey/username and
apisecret/password. For example, in order to add a Rackspace backend::

    mist add backend --name RackBackend --provider rackspace:ord --key rackspace_username --secret rackspace_secret_key

You can now see a list of all your added backends::

    mist list backends

Output::

    +---------------+------------------------------+------------------+--------+
    |      Name     |              ID              |     Provider     | State  |
    +---------------+------------------------------+------------------+--------+
    |   NephoScale  | W16qxKErSArH9DSNJyxXU81n35w  |    nephoscale    | online |
    |  DigitalOcean | 3aJhBzUtAMnCUmpEHKJsqLdm1Z9p |   digitalocean   | online |
    | Rackspace ORD | 2zMXgapqqaw9bSNUzSmuygFLy6Kp |    rackspace     | online |
    |      EC2      | D1g9abwqGUmQuZKGGBMfCgw8AUQ  | ec2_ap_northeast | online |
    |     Docker    | B3rbEA6bteaqMWJ4obVbgbqrXWf  |      docker      | online |
    |  Rackspace AU | 36vp27TVyUCarDNNcta1Knsqcr8Z |    rackspace     | online |
    +---------------+------------------------------+------------------+--------+

You can also display information about a specific backend, either by providing the backend's name or ID. The following
commands are equivalent::

    mist show backend --name EC2
    mist show backend --id D1g9abwqGUmQuZKGGBMfCgw8AUQ

Output::

    +--------------+------------------------------+-----------+--------+
    |    Title     |              ID              |  Provider | State  |
    +--------------+------------------------------+-----------+--------+
    | Rackspace AU | 36vp27TVyUCarDNNcta1Knsqcr8Z | rackspace | online |
    +--------------+------------------------------+-----------+--------+

    Machines:
    +------------------------+--------------------------------------+---------+------------------------------------------------------+
    |          Name          |                  ID                  |  State  |                      Public Ips                      |
    +------------------------+--------------------------------------+---------+------------------------------------------------------+
    | dbServer               | 9da278-48cf-4673-97-5b101db72769     | running | 119.19.32.217 -- 2400:1700:7000:100:fecc:c49c:28:892 |
    +------------------------+--------------------------------------+---------+------------------------------------------------------+

You have the option to rename a backend::

    mist rename backend --name EC2 --new_name RenamedBackend

Finally you can delete a backend. The following two commands are equivalent::

    mist delete backend --name DigitalOcean
    mist delete backend --id D1g9abwqGUmQuZKGGBMfCgw8AUQ

You can see a full use case `here`_

.. _here: http://asciinema.org/a/11875