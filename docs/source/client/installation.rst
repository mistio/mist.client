Installation
************

Install using pip
=================
This is the easiest way to obtain the mist package::

    pip install mist

You now have the ``mistclient`` module and the ``mist`` command line tool installed.

Bash completion
===============
To enable bash completion, you have to do the following::

    sudo activate-global-python-argcomplete

And then add the following line in your ``~/.bashrc``::

    eval "$(register-python-argcomplete  /usr/bin/mist)"

