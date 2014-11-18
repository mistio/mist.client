Getting Started with mist command
*********************************

The ``mist`` command line tool gets installed alongside mist package.

``mist`` will prompt for your mist email and password. At the end it will ask you to create a config file ``~/.mist``.
By having the config file you'll be able to use mist command without providing your credentials every time. The config
file will look like this::

    [mist.io]
    mist_uri=https://mist.io

    [mist.credentials]
    email=user@mist.io
    password=mist_password

.. Note:: *In case you have a private installation of mist.io you can change the mist_uri to point to your custom url*

.. Note:: The ``mist`` command line tool supports bash completion.

To enable auto-completion, you have to do the following::

    sudo activate-global-python-argcomplete

And then add the following line in your ``~/.bashrc``::

    eval "$(register-python-argcomplete  /usr/bin/mist)"


To see your accounts' specific information::

    mist user-info

Output::

    User Details:
    +---------+--------------+-------------------+--------------+------------------+
    | country | company_name | number_of_servers |     name     | number_of_people |
    +---------+--------------+-------------------+--------------+------------------+
    |  Greece |     Mist     |        1-5        | John Doe     |       1-5        |
    +---------+--------------+-------------------+--------------+------------------+

    Current Plan:
    +---------------+------------+---------+--------------------------+---------+-------------+---------------------------+
    | machine_limit | promo_code |  title  |         started          | isTrial | has_expired |         expiration        |
    +---------------+------------+---------+--------------------------+---------+-------------+---------------------------+
    |       20      |            | Startup | Mon Oct 28 18:49:50 2013 |   True  |    False    | Mon Jun 24 19:41:35 29393 |
    |               |            |         |                          |         |             |                           |
    +---------------+------------+---------+--------------------------+---------+-------------+---------------------------+

General Usage
=============
The command line tool is used as ``mist <action> [--extra-params...]``

For example:
::

    mist list-providers
    mist list-machines
    mist add-backend --name EC2 --provider ec2_ap_northeast --ec2-api-key IUOOLK9098OLIU --ec2-api-secret sahkjlhadoiu098098lLKlkjlkj
    mist delete-backend Rackspace
    mist create-machine --name dbServer
