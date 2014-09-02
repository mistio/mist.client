mist machines
*************
Now that you have added your backends and keys you can provision and monitor any machine on any of your providers.

Before you provision a machine, you'll need to provide some information, regarding the Image to use, the size of the machine
and on which Backend's location. All of these information differ with each provider. However you can list all of them and choose your desired values.

Images
======
To see all the available images for a backend::

    mist list images --backend DigitalOcean

The ``--backend`` option can be either the backend's id or name. Both will do.

The list of images can be huge, especially on providers such as EC2. My default mist.io will return a list of the most
used images. You can however use the ``--search`` option. If you provide ``--search all`` mist.io will provide all
available images. If you want to narrow your search you can search for a specific image::

    mist ls images --backend DigitalOcean --search all
    mist ls images --backend DigitalOcean --search gentoo

From the returned list you 'll need your desired image's ID to be used with machine creation.

Sizes - Locations/Regions
=========================
Each provider offers different options for machine sizes and locations/regions to choose from. For each of them you'll
need the corresponding ID::

    mist ls sizes --backend DigitalOcean
    mist ls locations --backend DigitalOcean

Create a new machine
====================
Now that you have gathered the information needed for machine creation you can tell mist to provision a machine on a
specific backend. Alongside the image, location and size ID's you'll also need to provide a keys' name to be assigned to
the newly created machine::

    mist create machine --backend EC2 --name dev.machine --image ami-bddaa2bc --size t1.micro --location 0 --key MyKey

Machine Actions
===============
You can list all your machines on all your Backends, or list machines on a specific backend::

    mist ls machines
    mist ls machines --backend Docker
You can start, stop, reboot or destroy a machine::

    mist reboot machine --backend Docker --name db-server-1
    mist destroy machine --backend Docker --name db-server-1

You can also probe a machine. By probing a machine you verify that sshd is up an running and that you have access to the
machine with the previously assigned key. A successful probe will return the machine's uptime::

    mist probe machine --name db-server-1 --backend Docker


You can see a full example `here`_

.. _here: http://asciinema.org/a/11885