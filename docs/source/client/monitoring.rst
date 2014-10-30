Monitoring
**********

Enable monitoring
=================
In case you have an account with the mist.io service (https://mist.io), you can enable monitoring to a machine::

    machine.enable_monitoring()

This will take some time, cause mist.io will auto-install collectd and configure it to send monitoting data to mist.io
servers. One way to see that the process has finished and you have data coming is::

    machine.get_stats()

In case enabling monitoring has finished you'll get your monitoring data in a dict.

Advanced monitoring options
===========================
By default, mist.io's collectd will be configured with some metrics, like Disk usage, CPU usage etc. However, mist.io
supports a huge list of collectd plugins that you can choose from::

    machine.available_metrics

Using your desired metric id, you can add that to a monitored machine. For example to have data about the number of
users that are currently logged in, we can use the ``users`` metric::

    machine.add_metric("users")

Custom metrics
==============
Since the last updates of mist.io, you can now upload custom python metrics that can literally monitor anything. These
plugins are simple python files that you can upload to the machine. They can be as simple as::

    import random

    def read():
        # return random value
        return random.random()

Or more complex, taking care of pings to other servers etc.

To upload a custom plugin to a monitored machine, all you need is the python file's path in your computer, and a name
for the plugin::

    machine.add_python_plugin(name="Random", python_file="/home/user/random.py")

Some more advanced options can be used, determining the value_type, the unit etc. You can see ``mistclient.model.Machine.add_python_plugin``
method for more info.
