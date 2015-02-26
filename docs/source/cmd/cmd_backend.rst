Backends
********

With mist you can handle multiple machines on multiple providers from one interface, the mist.io service.
In order to do so, the very first thing to do when using mist.io is to ensure that you have added your backends.
After doing that you'll be able to provision, monitor and in general handle all your machines on all
those providers.

Supported Providers
===================
Before you add a new backend, you'll find it useful to see a list of all the providers that mist.io supports::

    mist list-providers

Output::

    Other Server                   bare_metal
    Azure                          azure
    EC2                            ec2                  Tokyo                ec2_ap_northeast
    EC2                            ec2                  Singapore            ec2_ap_southeast
    EC2                            ec2                  Sydney               ec2_ap_southeast_2
    EC2                            ec2                  Ireland              ec2_eu_west
    EC2                            ec2                  Sao Paulo            ec2_sa_east
    EC2                            ec2                  N. Virginia          ec2_us_east
    EC2                            ec2                  N. California        ec2_us_west
    EC2                            ec2                  Oregon               ec2_us_west_oregon
    Google Compute Engine          gce
    NephoScale                     nephoscale
    DigitalOcean                   digitalocean
    Linode                         linode
    OpenStack                      openstack
    Rackspace                      rackspace            Dallas               dfw
    Rackspace                      rackspace            Chicago              ord
    Rackspace                      rackspace            N. Virginia          iad
    Rackspace                      rackspace            London               lon
    Rackspace                      rackspace            Sydney               syd
    Rackspace                      rackspace            Hong Kong            hkg
    Rackspace                      rackspace            US-First Gen         rackspace_first_gen:us
    Rackspace                      rackspace            UK-First Gen         rackspace_first_gen:uk
    SoftLayer                      softlayer
    HP Helion Cloud                hpcloud              US West              region-a.geo-1
    HP Helion Cloud                hpcloud              US East              region-b.geo-1
    Docker                         docker
    VMware vCloud                  vcloud
    Indonesian Cloud               indonesian_vcloud
    KVM (via libvirt)              libvirt


.. Note:: With every *list* action, you can have the output in a more *pretty* format by providing the ``--pretty`` flag.

For example, ``mist list-providers --pretty`` will return this output::

    +-----------------------+-------------------+---------------+------------------------+
    |        Provider       |    Provider ID    |     Region    |       Region ID        |
    +-----------------------+-------------------+---------------+------------------------+
    |      Other Server     |     bare_metal    |       -       |           -            |
    |         Azure         |       azure       |       -       |           -            |
    |          EC2          |        ec2        |     Tokyo     |    ec2_ap_northeast    |
    |          EC2          |        ec2        |   Singapore   |    ec2_ap_southeast    |
    |          EC2          |        ec2        |     Sydney    |   ec2_ap_southeast_2   |
    |          EC2          |        ec2        |    Ireland    |      ec2_eu_west       |
    |          EC2          |        ec2        |   Sao Paulo   |      ec2_sa_east       |
    |          EC2          |        ec2        |  N. Virginia  |      ec2_us_east       |
    |          EC2          |        ec2        | N. California |      ec2_us_west       |
    |          EC2          |        ec2        |     Oregon    |   ec2_us_west_oregon   |
    | Google Compute Engine |        gce        |       -       |           -            |
    |       NephoScale      |     nephoscale    |       -       |           -            |
    |      DigitalOcean     |    digitalocean   |       -       |           -            |
    |         Linode        |       linode      |       -       |           -            |
    |       OpenStack       |     openstack     |       -       |           -            |
    |       Rackspace       |     rackspace     |     Dallas    |          dfw           |
    |       Rackspace       |     rackspace     |    Chicago    |          ord           |
    |       Rackspace       |     rackspace     |  N. Virginia  |          iad           |
    |       Rackspace       |     rackspace     |     London    |          lon           |
    |       Rackspace       |     rackspace     |     Sydney    |          syd           |
    |       Rackspace       |     rackspace     |   Hong Kong   |          hkg           |
    |       Rackspace       |     rackspace     |  US-First Gen | rackspace_first_gen:us |
    |       Rackspace       |     rackspace     |  UK-First Gen | rackspace_first_gen:uk |
    |       SoftLayer       |     softlayer     |       -       |           -            |
    |    HP Helion Cloud    |      hpcloud      |    US West    |     region-a.geo-1     |
    |    HP Helion Cloud    |      hpcloud      |    US East    |     region-b.geo-1     |
    |         Docker        |       docker      |       -       |           -            |
    |     VMware vCloud     |       vcloud      |       -       |           -            |
    |    Indonesian Cloud   | indonesian_vcloud |       -       |           -            |
    |   KVM (via libvirt)   |      libvirt      |       -       |           -            |
    +-----------------------+-------------------+---------------+------------------------+


From here on you'll need your desired provider's id in order to use it when adding a new backend.

Backend Actions
===============

Add an EC2 backend::

    mist add-backend --provider ec2 --region ec2_ap_northeast --ec2-api-key AKIAHKIB7OIJCX7YLIO3JA --ec2-api-secret knbkGJKHG9gjhUuhgfjtiu987

Add a Rackspace backend::

    mist add-backend --provider rackspace --region iad --rackspace-username my_username --rackspace-api-key 098er098eqwec98dqdqd098

Add a Nephoscale backend::

    mist add-backend --provider nephoscale --nepho-username nepho_username --nepho-password nepho_passwd

Add a DigitalOcean backend::

    mist add-backend --provider digitalocean --digi-token kjhdkfh897dfodlkfjlkhdf90sdfusldkfjkljsdf098lkjlkj

Add a Linode backend::

    mist add-backend --provider linode --linode-api-key dkljflkjlkgddgijgd00987ghudGgcf9Glkjh

Add an OpenStack backend::

    mist add-backend --provider openstack --openstack-username demo --openstack-password mypass --openstack-auth-url http://10.0.0.1:5000 --openstack-tenant demo

Add a Softlayer backend::

    mist add-backend --provider softlayer --softlayer-username soft_username --softlayer-api-key kjhfdkjahf098OIjhkFChiugiGIIUuoh

Add a HP Cloud backend::

    mist add-backend --provider hpcloud --region region-a.geo-1 --hp-username hp_username --hp-password my_pass --hp-tenant my_tenant

Add a Azure backend::

    To add a Azure backend you have to download to a file the Azure certificate.

    mist add-backend --provider azure --azure-sub-id lkjoiy8-kjdjkhd-987-hd9d --azure-cert-path /home/user/azure.cert

Add a Docker backend::

    mist add-backend --provider docker --docker-host 10.0.0.1 --docker-port 4243

Add a Bare Metal Server (or any server)::

    mist add-backend --provider bare_metal --bare-hostname 198.230.89.3 --bare-user root --bare-port 22 --bare-ssh-key-id my_ssh_key

Add a Google Compute Engine backend::

    To add a GCE backend you have to download the private key file

    mist add-backend --provider gce --gce-email 46234234246-3oiuoiu0980989873yui@developer.gserviceaccount.com --gce-project-id gifted-electron-10 --gce-private-key /home/user/gce.key

Add VMware(vCloud) backend::

    mist add-backend --provider vcloud --vcloud-username admin --vcloud-password ioiuYoiuOIU --vcloud-organization MyOrg.io --vcloud-host compute.idcloudonline.com

Add Indonesian vCloud backend::

    mist add-backend --provider indonesian_vcloud --indonesian-username admin --indonesian-password kjOIULKJLlkj --indonesian-organization MyOrg.io

Add KVM(via libvirt) backend::

    mist add-backend --provider libvirt --libvirt-hostname 10.0.0.1 --libvirt-user root --libvirt-key MyAddedKey


You can now see a list of all your added backends::

    mist list-backends


Output::

    openstackaf0.mist.io                     2Mn2ZnCoXhK3ywqzGn1fzWVmSSe6             bare_metal                     online
    Icehouse                                 4ukW6Juooqa8bTu2YgM4mE8RAsk7             openstack                      online
    EC2 AP Sydney                            25ykPERh5D17DyoeKsCgw35DLmvw             ec2_ap_southeast_2             online
    Openstack Juno                           2u5yKqXmDiZ7BHCk1u17FFcmFS2m             openstack                      online
    HP Helion Cloud                          3WwgPBXETjdeMEbM5fUCACSvedGT             hpcloud                        online
    Google Compute Engine                    g6T3HYae2ZMcHfHyFGKVtMG6PZU              gce                            online
    Docker                                   B3rbEA6bteaqMWJ4obVbgbqrXWf              docker                         online
    openstackdfe.mist.io                     XMdRN2u3NVASMm14BuHo4HJnS15              bare_metal                     online


.. Note:: You can use the ``--pretty`` flag. ``mist list-backends --pretty`` will return:

::

    +-----------------------+------------------------------+--------------------+--------+
    |          Name         |              ID              |      Provider      | State  |
    +-----------------------+------------------------------+--------------------+--------+
    |  openstackaf0.mist.io | 2Mn2ZnCoXhK3ywqzGn1fzWVmSSe6 |     bare_metal     | online |
    |        Icehouse       | 4ukW6Juooqa8bTu2YgM4mE8RAsk7 |     openstack      | online |
    |     EC2 AP Sydney     | 25ykPERh5D17DyoeKsCgw35DLmvw | ec2_ap_southeast_2 | online |
    |     Openstack Juno    | 2u5yKqXmDiZ7BHCk1u17FFcmFS2m |     openstack      | online |
    |    HP Helion Cloud    | 3WwgPBXETjdeMEbM5fUCACSvedGT |      hpcloud       | online |
    | Google Compute Engine | g6T3HYae2ZMcHfHyFGKVtMG6PZU  |        gce         | online |
    |         Docker        | B3rbEA6bteaqMWJ4obVbgbqrXWf  |       docker       | online |
    |  openstackdfe.mist.io | XMdRN2u3NVASMm14BuHo4HJnS15  |     bare_metal     | online |
    +-----------------------+------------------------------+--------------------+--------+


You can also display information about a specific backend, either by providing the backend's name or ID. The following
commands are equivalent::

    mist describe-backend Icehouse
    mist describe-backend 4ukW6Juooqa8bTu2YgM4mE8RAsk7
    mist describe-backend --id 4ukW6Juooqa8bTu2YgM4mE8RAsk7
    mist describe-backend --name Icehouse

Output::

    +----------+------------------------------+-----------+--------+
    |  Title   |              ID              |  Provider | State  |
    +----------+------------------------------+-----------+--------+
    | Icehouse | 4ukW6Juooqa8bTu2YgM4mE8RAsk7 | openstack | online |
    +----------+------------------------------+-----------+--------+

    Machines:
    +---------+--------------------------------------+---------+-------------+
    |   Name  |                  ID                  |  State  |  Public Ips |
    +---------+--------------------------------------+---------+-------------+
    | atlanta | c9411bbe-2bb2-4a88-996c-d831272b426e | running | 109.59.77.32|
    +---------+--------------------------------------+---------+-------------+


You have the option to rename a backend::

    mist rename-backend Icehouse --new-name Openstack_Icehouse

Finally you can delete a backend. The following two commands are equivalent::

    mist delete-backend Docker

