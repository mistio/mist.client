Monitoring
**********
`Mist.io`_ offers plans for monitoring your machines. By default it will install a ``collectd`` instance pre-configured with some basic
metrics and send the results to mist.io's servers. By visiting mist.io you can see live graphs of your monitored machines.

.. _Mist.io: https://mist.io

Furthermore, you have a huge list of collectd plugins that you can add to your machine and even upload custom pyton scripts to be
used as collectd plugins, allowing you to monitor...well, almost everything.

Enable monitoring
=================
In order to enable monitoring on a machine with name ``dbServer``::

    mist enable-monitoring dbServer

Now, your dbServer machine has collectd installed and you can visit mist.io to see live graphs (note that the first time
you enable collectd it may take some time for the package to install).

To disable monitoring on a machine::

    mist disable-monitoring dbServer


Add Metrics
===========
Collectd supports a huge list of custom metrics/plugins. To see all available plugins/metrics for a monitored machine::

    mist list-metrics --machine dbServer

If you wish to add one of those metrics you have to use the metric's id. For example, to add the metric ``users``::

    mist add-metric --machine dbServer --metric-id users

Mist.io supports custom, python plugins. For example, if you have a ``~/plugin.py``::

    import random

    def read():
        # return random value
        return random.random()

You can add it by providing the ``--custom_plugin`` parameter and providing a plugin name with the ``--plugin`` parameter::

    mist add-custom-metric --machine dbServer --metric-name my_custom_metric --file-path ~/plugin.py --unit my_unit

