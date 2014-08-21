mist.client
===========

Python Client for mist.io

The MistClient
===========

```
from mist.client import MistClient

client = MistClient(email="account@mail.com", password="mypassword")

```

In case you have a custom installation of mist.io (see: https://github.com/mistio/mist.io on how to run mist.io on your own server) you could explicitly give another uri for the service:

```
client = MistClient(mist_uri="http://localhost:8000")
```

