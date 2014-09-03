mist machines
*************
Now that you have added your backends and keys you can provision and monitor any machine on any of your providers.

Before you provision a machine, you'll need to provide some information, regarding the OS Image to use, the size of the machine
and on which Backend's location. All of these information differ with each provider. However you can list all of them and choose your desired values.

Images
======
To see all the available images for a backend. *The* ``--backend`` *option can be either the backend's id or name. Both will do.*
::

    mist list images --backend DigitalOcean


Output::

    +--------------------------------------+-----+
    |                 Name                 |  ID |
    +--------------------------------------+-----+
    |       Linux CentOS 5.5 32-bit        |  3  |
    |       Linux CentOS 5.5 64-bit        |  5  |
    |   Linux Debian Server 5.05 32-bit    |  23 |
    | Linux Ubuntu Server 10.04 LTS 32-bit |  43 |
    |       Linux CentOS 5.7 32-bit        |  45 |
    | Linux Ubuntu Server 10.04 LTS 64-bit |  49 |
    |   Linux Debian Server 6.0.3 64-bit   |  51 |
    |      Linux Debian 5.0.9 64-bit       |  55 |
    |      Linux Debian 5.0.9 32-bit       |  57 |
    |       Linux CentOS 6.2 64-bit        |  59 |
    |       Linux CentOS 5.8 64-bit        |  64 |
    | Linux Ubuntu Server 12.04 LTS 64-bit |  75 |
    |  VOD Cloud Storage Proxy (FTP:HTTP)  | 101 |
    |    Linux Debian Server 7.1 64-bit    | 177 |
    |       Linux CentOS 5.10 64-bit       | 269 |
    |       Linux CentOS 6.5 64-bit        | 271 |
    |       Ubuntu Server 14.04 LTS        | 317 |
    +--------------------------------------+-----+


The list of images can be huge, especially on providers such as EC2. My default mist.io will return a list of the most
used images. You can however use the ``--search`` option. If you provide ``--search all`` mist.io will provide all
available images. If you want to narrow your search you can search for a specific image::

    mist list images --backend DigitalOcean --search all
    mist list images --backend DigitalOcean --search gentoo

From the returned list you 'll need your desired image's ID to be used with machine creation.

Sizes - Locations/Regions
=========================
Each provider offers different options for machine sizes and locations/regions to choose from. For each of them you'll
need the corresponding ID::

    mist list sizes --backend DigitalOcean

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

    mist ls locations --backend DigitalOcean

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

    mist create machine --backend EC2 --name dev.machine --image ami-bddaa2bc --size t1.micro --location 0 --key MyKey

Machine Actions
===============
You can list all your machines on all your Backends, or list machines on a specific backend::

    mist list machines
    mist list machines --backend Docker
You can start, stop, reboot or destroy a machine::

    mist reboot machine --backend Docker --name db-server-1
    mist destroy machine --backend Docker --name db-server-1

You can also probe a machine. By probing a machine you verify that sshd is up an running and that you have access to the
machine with the previously assigned key. A successful probe will return the machine's uptime::

    mist probe machine --name db-server-1 --backend Docker


After creating a new machine it might take a little time for the probe to be successful.


You can see a full example `here`_

.. _here: http://asciinema.org/a/11885