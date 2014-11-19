Machines
********
Now that you have added your backends and keys you can provision and monitor any machine on any of your providers.

Before you provision a machine, you'll need to provide some information, regarding the OS Image to use, the size of the machine
and on which Backend's location. All of these information differ with each provider. However you can list all of them and choose your desired values.

Images
======
To see all the available images for a backend. *The* ``--backend`` *option can be either the backend's id or name. Both will do.*
::

    mist list-images --backend Juno


Output::

    Fedora-x86_64-20-20140618-sda            755c8a98-882f-4dd2-9598-5c01c039e63a
    cirros-0.3.2-x86_64-uec                  cbcc00f7-6ec0-41a5-ad42-3008143a77b2
    cirros-0.3.2-x86_64-uec-ramdisk          586360b9-06f4-4353-9f62-7191a9f95d64
    cirros-0.3.2-x86_64-uec-kernel           475ae832-7d2a-4b0b-a4d9-63e7d170a223

And with the ``--pretty`` flag, ``mist list-images --backend Juno --pretty``::

    +---------------------------------+--------------------------------------+
    |               Name              |                  ID                  |
    +---------------------------------+--------------------------------------+
    |  Fedora-x86_64-20-20140618-sda  | 755c8a98-882f-4dd2-9598-5c01c039e63a |
    |     cirros-0.3.2-x86_64-uec     | cbcc00f7-6ec0-41a5-ad42-3008143a77b2 |
    | cirros-0.3.2-x86_64-uec-ramdisk | 586360b9-06f4-4353-9f62-7191a9f95d64 |
    |  cirros-0.3.2-x86_64-uec-kernel | 475ae832-7d2a-4b0b-a4d9-63e7d170a223 |
    +---------------------------------+--------------------------------------+
The list of images can be huge, especially on providers such as EC2. My default mist.io will return a list of the most
used images. You can however use the ``--search`` option. If you provide ``--search all`` mist.io will provide all
available images. If you want to narrow your search you can search for a specific image::

    mist list-images --backend DigitalOcean --search all
    mist list-images --backend DigitalOcean --search gentoo

From the returned list you 'll need your desired image's ID to be used with machine creation.

Sizes - Locations/Regions
=========================
Each provider offers different options for machine sizes and locations/regions to choose from. For each of them you'll
need the corresponding ID::

    mist list-sizes --backend DigitalOcean
    mist list-sizes --backend DigitalOcean --pretty

Output::

    +---------------------------------------------+-----+
    |                     Name                    |  ID |
    +---------------------------------------------+-----+
    |    CS05-SSD - 0.5GB, 1Core, 25GB, 10 Gbps   | 219 |
    |     CS1-SSD - 1GB, 1Core, 25GB, 10 Gbps     | 221 |
    |    CS2.1-SSD - 2GB, 1Core, 37GB, 10 Gbps    | 223 |
    |    CS2.2-SSD - 2GB, 2Core, 50GB, 10 Gbps    | 225 |
    |    CS4.2-SSD - 4GB, 2Core, 75GB, 10 Gbps    | 227 |
    |    CS4.4-SSD - 4GB, 4Core, 100GB, 10 Gbps   | 229 |
    |    CS8.4-SSD - 8GB, 4Core, 150GB, 10 Gbps   | 231 |
    |    CS8.8-SSD - 8GB, 8Core, 200GB, 10 Gbps   | 233 |
    |   CS16.8-SSD - 16GB, 8Core, 300GB, 10 Gbps  | 235 |
    |  CS16.16-SSD - 16GB, 16Core, 400GB, 10 Gbps | 237 |
    |   CS32.8-SSD - 32GB, 8Core, 600GB, 10 Gbps  | 239 |
    |  CS32.16-SSD - 32GB, 16Core, 800GB, 10 Gbps | 241 |
    | CS64.20-SSD - 64GB, 20Core, 1600GB, 10 Gbps | 243 |
    |      CS05 - 0.5GB, 1Core, 25GB, 1 Gbps      |  5  |
    |        CS1 - 1GB, 1Core, 50GB, 1 Gbps       |  3  |
    |       CS2.1 - 2GB, 1Core, 75GB, 1 Gbps      |  46 |
    |      CS2.2 - 2GB, 2Core, 100GB, 1 Gbps      |  7  |
    |      CS4.2 - 4GB, 2Core, 150GB, 1 Gbps      |  48 |
    |      CS4.4 - 4GB, 4Core, 200GB, 1 Gbps      |  9  |
    |      CS8.4 - 8GB, 4Core, 300GB, 1 Gbps      |  50 |
    |      CS8.8 - 8GB, 8Core, 400GB, 1 Gbps      |  11 |
    |     CS16.8 - 16GB, 8Core, 600GB, 1 Gbps     |  52 |
    |    CS16.16 - 16GB, 16Core, 800GB, 1 Gbps    |  1  |
    |     CS32.8 - 32GB, 8Core, 1000GB, 1 Gbps    |  56 |
    |    CS32.16 - 32GB, 16Core, 1200GB, 1 Gbps   |  54 |
    +---------------------------------------------+-----+


::

    mist list-locations --backend DigitalOcean
    mist list-locations --backend DigitalOcean --pretty

Output::

    +-------+-------+
    |  Name |   ID  |
    +-------+-------+
    | SJC-1 | 86945 |
    | RIC-1 | 87729 |
    +-------+-------+

Create a new machine
====================
Now that you have gathered the information needed for machine creation you can tell mist to provision a machine on a
specific backend. Alongside the image, location and size ID's you'll also need to provide a keys' name to be assigned to
the newly created machine::

    mist create-machine --backend EC2 --name dev.machine --image ami-bddaa2bc --size t1.micro --location 0 --key MyKey

Machine Actions
===============
You can list all your machines on all your Backends, or list machines on a specific backend::

    mist list-machines
    mist list-machines --backend Docker

You can start, stop, reboot or destroy a machine. To specify a machine you can either directly use the machine's name
or ID, or pass the ``--id``, ``--name`` flags::

    mist reboot db-server-1
    mist destroy db-server-1

You can also probe a machine. By probing a machine you verify that sshd is up an running and that you have access to the
machine with the previously assigned key::

    mist probe db-server-1


After creating a new machine it might take a little time for the probe to be successful.

You can also tag machine::

    mist tag db-server-1 --new-tag dbservers

Tagging will be useful later when you want to group your machines across different clouds and run multiple commands
and configuration scripts.