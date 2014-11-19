Changelog
*********

Release 0.3.0 (released Nov 18,2014)
====================================

Featured added:

* Repackage ``mist.client`` to ``mist``
* Refactor  ``mistclient.machines`` and ``mistclient.backends``
* ``client.machines``, ``client.backends``, ``client.keys`` are now lists instead of dicts
* Refactor the  ``mist`` command line tool
* Add ``mist run`` capability

Release 0.1.0 (released Sep 3, 2014)
====================================

Features added:

* ``mist`` command line interface
* Add ``client.backend_from_name``, ``client.backend_from_id`` and ``client.search_backend methods``
* Add ``backend.machine_from_name``, ``backend.machine_from_id``, ``backend.machine_from_ip`` and ``backend.search_machine`` methods
* ``client.backends`` is now a dict with backend ids as dict.keys
* ``backend.machines`` is now a dict with machine ids as dict.keys

Bugs fixed:

* `#5`_: Fix pip hanging up when installing requirements for the first time
* `#6`_: Fix ``mist sync`` when syncing Bare Metal Backends

.. _#5: https://github.com/mistio/mist.client/issues/5
.. _#6: https://github.com/mistio/mist.client/issues/6