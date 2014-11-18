Keys
****

By uploading your SSH keys to mist.io you can access all your machines through mist.io, have a shell prompt from your browser
and even let mist.io take care of enabling monitoring to your machines. You also can have mist.io run commands to your machines
during provisiong or after an alert is triggered.

Add a new key
=============
When adding a new key, you have 2 choices. Either upload a local ssh-key to mist.io, or ask mist.io to generate one
for you.

When uploading a local ssh-key, you have to provide the private ssh-key as a string. So first you can::

    with open("/home/user/.ssh/my_key") as f:
        private = f.read()

You now have the private key and can add a new key to mist.io::

    client.add_key(key_name="MyKey", private=private)

Or have mist.io generate a randon one for you::

    private = client.generate_key()
    client.add_key(key_name="MyKey", private=private)

After adding a new key, client.keys will be automatically updated.

Keys actions
============
To see all added keys::

    client.keys()

The result will be a list like this::

    [Key => Dummy,
     Key => ParisDemo2,
     Key => testkey,
     Key => DemoKey,
     Key => TestKey,
     Key => ParisDemo]

You can now search for key names::

    key = client.keys(search="Paris")[0]

You have the option to set a key as the default one. This becomes handy if you want mist.io to auto-assign this key to
a machine if you leave the association blank::

    key.set_default()

You can rename the key::

    key.rename("newName")


Finally, to delete the key::

    key.delete()

See ``mistclient.model.Key`` class for detailed information.
