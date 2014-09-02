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

.. _here: http://asciinema.org/a/11874