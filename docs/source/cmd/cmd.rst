Getting Started with mist command
*********************************

The mist.client package, when installed, installs alongside the ``mist`` command.

The ``mist`` command line tool will look for the config file ~/.mist::

    [mist.io]
    mist_uri=https://mist.io

    [mist.credentials]
    email=bluebusforever@gmail.com
    password=lida1234

If no file is found, then it will fall back in interactive mode and ask for email and password.

For an example you can see `here`_

.. _here: http://asciinema.org/a/11883


To see your accounts specific information::

    mist user info


General Usage
=============
The command line tool is used in as ``mist <action> <target> [--extra-params...]``

List backends, machines, keys:

* mist list
* mist ls
::

    mist ls providers


Display specific information:

* mist show
* mist display
* mist describe
::

    mist show backend --name EC2NorthEast


Add backends, keys, machines:

* mist add
* mist create
::

    mist add backend --name EC2 --provider ec2_ap_northeast --key IUOOLK9098OLIU --secret sahkjlhadoiu098098lLKlkjlkj


Delete/remove:

* mist rm
* mist delete
* mist del
* mist remove
::

    mist rm backend --id 3aJoiuYB9mpEHKJsqLdm1Z9p

