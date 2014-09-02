mist monitoring
***************
`Mist.io`_ offers plans for monitoring your machines. By default it will install a ``collectd`` instance pre-configured with some basic
metrics and send the results to mist.io's servers. By visiting mist.io you can see live graphs of your monitored machines.

.. _Mist.io: https://mist.io

Furthermore, you have a huge list of collectd plugins that you can add to your machine and even upload custom pyton scripts to be
used as collectd plugins, allowing you to monitor...well, almost everything.

Enable monitoring
=================
In order to enable monitoring on a machine::

    mist enable-monitoring machine --backend EC2 --name dbServer

Now, your dbServer machine has collectd installed and you can visit mist.io to see live graphs (note that the first time
you enable collectd it may take some time for the package to install).

To disable monitoring on a machine::

    mist disable-monitoring machine --backend EC2 --name dbServer


Add Plugins
===========
Collectd supports a huge list of custom plugins. To see all available plugins for a monitored machine::

    mist ls plugins --backend EC2 --name dbServer

If you wish to add one of those plugins you have to use the plugin's id. For example, to add the plugin ``users``::

    mist add plugin --backend EC2 --name dbServer --plugin users

Mist.io supports custom, python plugins. For example, if you have a ``~/plugin.py``::

    import random

    def read():
        # return random value
        return random.random()

You can add it by providing the ``--custom_plugin`` parameter and providing a plugin name with the ``--plugin`` parameter::

    mist add plugin --backend EC2 --name dbServer --plugin MyPlugin --custom_plugin ~/plugin.py


*Note: mist.io supports adding rules and actions for your monitored machines. The mist command line tool will support
those features together with viewing your current monitor stats in the next major release*