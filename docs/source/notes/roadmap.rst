Roadmap
*******

Upcoming Release 0.1.2
======================

Features to be added:

* Save api_token in tmp file and use it to reconnect rather than opening a new connection upon each request
* Add ansible capabilities to ``mist`` command (.e.g ``mist run ansible playbook.yml``)

Upcoming Release 0.1.1
======================

Features to be added:

* Integrate the functionality to add rules from both ``mist.client`` Python interface and ``mist`` command line interface
* Use ``mist`` command line tool to automatically open an ssh connection to a machine (e.g. ``mist connect machine``)
* See real time stats from monitored machines in terminal with ``mist show stats``
* Refactor duplicate code in ``mist.cmd.helpers`` methods
* Add option to connect to https installations of mist.io with self-signed certificate (option in config file)