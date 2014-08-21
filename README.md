mist.client
===========

Python Client for mist.io

Example usage
===========

```
# This is an simple example of how to reboot
# a machine using mist client

from mist.client import MistClient

client = MistClient(email="account@mail.com", password="mypassword")

backend = client.backends['EC2']

machine = backend.machines['mist-vm']
machine.reboot()
```
