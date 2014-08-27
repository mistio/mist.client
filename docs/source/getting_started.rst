Getting Started
***************

Now that you have the ``mist.client`` package you can import it to use it::

    from mist.client import MistClient
    client = MistClient(email="yourmail@mist.io", password="yourpassword")

By default ``MistClient`` will try to connect to the mist.io service, with default url set to https://mist.io. However,
you may have a custom, in-house installation of mist.io as described here: https://github.com/mistio/mist.io. In this
case you may change the url and even leave email and password blank (if it is an in-house installation without
authentication)::

    client = MistClient(mist_uri="http://localhost:8000")

