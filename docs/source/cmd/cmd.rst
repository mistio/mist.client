Introduction
************

``mist`` will prompt for your mist.io email and password. You have the option to create a config file at ``~/.mist``.
By having this config file you'll be able to use the mist command without providing your credentials every time. The config
file will look like this::

    [mist.credentials]
    email=user@mist.io
    password=mist_password


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


