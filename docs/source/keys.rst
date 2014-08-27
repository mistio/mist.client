Keys
****

SSH Keys are needed in order to have full access to your provisioned machines. Those are stored securely by the mist.io
service and you can use them to provision any machine in any provider.

Add a new key
=============
When adding a new key, you have 2 choices. Either upload a local ssh-key to mist.io, or ask mist.io to generate one
for you.

When uploading a local ssh-key, you have to provide the private ssh-key as a string to mist.io. So first you can::

    with open("/home/user/.ssh/my_key") as f:
        private = f.read()

You now have the private key and can add a new key to mist.io::

    client.add_key(key_name="MyKey", private=private)

Or have mist.io generate a randon one for you::

    private = client.generate_key()
    client.add_key(key_name="MyKey", private=private)

After adding a new key, you have to update the client's keys list::

    client.update_keys()


Keys actions
============
To see all added keys::

    client.keys

The result will be a dict like this::

    {u'MyKey': Key => MyKey, u'asd': Key => asd, u'newKey': Key => newKey}

You can now choose a key::

    key = client.keys['MyKey']

You have the option to set a key as the default one. This becomes handy if you want mist.io to auto-assign this key to
a machine if you leave the association blank::

    key.set_default()

Finally, to delete the key::

    key.delete()

See `Key`_ class for detailed information.

.. _Key: mist.client.html#mist.client.model.Key