Sync
****
``mist sync`` is used when you have such a custom installation of mist.io that keeps all of the data in a yaml file
In case you want to sync your local db.yaml with your account in https://mist.io you could use the ``sync``
action::

    mist sync dbyaml --dbyaml /path/to/local/db.yaml


``mist sync`` will only add Keys and Backends that are added in your local mist.io installation and not in the `mist.io`_
service. It will not remove Backends and Keys that are added in the service and are absent in your local installation.

.. _mist.io: https://mist.io