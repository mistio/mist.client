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

Add an EC2 backend::

    mist add-backend --provider ec2_ap_northeast --ec2-api-key AKIAHKIB7OIJCX7YLIO3JA --ec2-api-secret knbkGJKHG9gjhUuhgfjtiu987

Add a Rackspace backend::

    mist add-backend --provider rackspace:iad --rackspace-username my_username --rackspace-api-key 098er098eqwec98dqdqd098

Add a Nephoscale backend::

    mist list backends --provider nephoscale --nepho-username nepho_username --nepho-password nepho_passwd

Add a DigitalOcean backend::

    mist add-backend --provider digitalocean --digi-token kjhdkfh897dfodlkfjlkhdf90sdfusldkfjkljsdf098lkjlkj

Add a Linode backend::

    mist add-backend --provider linode --linode-api-key dkljflkjlkgddgijgd00987ghudGgcf9Glkjh

Add an OpenStack backend::

    mist add-backend --provider openstack --openstack-username demo --openstack-password mypass --openstack-auth-url http://10.0.0.1:5000 --openstack-tenant demo

Add a Softlayer backend::

    mist add-backend --provider softlayer --softlayer-username soft_username --softlayer-api-key kjhfdkjahf098OIjhkFChiugiGIIUuoh

Add a HP Cloud backend::

    mist add-backend --provider hpcloud:region-a.geo-1 --hp-username hp_username --hp-password my_pass --hp-tenant my_tenant

Add a Azure backend::

    To add a Azure backend you have to download to a file the Azure certificate.

    mist add-backend --provider azure --azure-sub-id lkjoiy8-kjdjkhd-987-hd9d --azure-cert-path /home/user/azure.cert

Add a Docker backend::

    mist add-backend --provider docker --docker-host 10.0.0.1 --docker-port 4243

Add a Bare Metal Server (or any server)::

    mist add-backend --provider bare_metal --bare-hostname 198.230.89.3 --bare-user root --bare-port 22 --bare-ssh-key-id my_ssh_key


You can now see a list of all your added backends::

    mist list-backends


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