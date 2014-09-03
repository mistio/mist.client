Getting Started with mist command
*********************************

The ``mist`` command line tool gets installed alongside mist.client package.

``mist`` will prompt for your mist email and password. At the end it will ask you to create a config file ``~/.mist``.
By having the config file you'll be able to use mist command without providing your credentials every time. The config
file will look like this::

    [mist.io]
    mist_uri=https://mist.io

    [mist.credentials]
    email=user@mist.io
    password=mist_password

.. Note:: *In case you have a private installation of mist.io you can change the mist_uri to point to your custom url*

To see your accounts' specific information::

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

