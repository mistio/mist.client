.. _mist_keys:


mist_keys - Manage ssh-keys from mist.io service
++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1

Synopsis
--------

.. versionadded:: 1.7.1

By uploading your SSH keys to mist.io you can access all your machines through mist.io, have a shell prompt from your browser and even let mist.io take care of enabling monitoring to your machines.
You also can have mist.io run commands to your machines during provisiong or after an alert is triggered.
*mist_email* and *mist_password* can be skipped if *~/.mist* config file is present.
See documentation for config file http://mistclient.readthedocs.org/en/latest/cmd/cmd.html

Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
            <tr>
    <td>auto_generate</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>If <em>True</em> it will ask mist.io to randomly generate a key and save it to the added keys</td>
    </tr>
            <tr>
    <td>key</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>When adding a new key, you can provide a local key's path to add to mist.io</td>
    </tr>
            <tr>
    <td>local_save_path</td>
    <td>no</td>
    <td>~/.ssh</td>
        <td><ul></ul></td>
        <td>If <em>save_locally</em>, the local save path will be used to save the key</td>
    </tr>
            <tr>
    <td>mist_email</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Email to login to the mist.io service</td>
    </tr>
            <tr>
    <td>mist_password</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Password to login to the mist.io service</td>
    </tr>
            <tr>
    <td>mist_uri</td>
    <td>no</td>
    <td>https://mist.io</td>
        <td><ul></ul></td>
        <td>Url of the mist.io service. By default https://mist.io. But if you have a custom installtion of mist.io you can provide the url here</td>
    </tr>
            <tr>
    <td>name</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Name of the key to add or list</td>
    </tr>
            <tr>
    <td>save_locally</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>If <em>True</em> the auto generated key will be saved locally</td>
    </tr>
            <tr>
    <td>state</td>
    <td>no</td>
    <td></td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td>If provided it will instruct the module to tirgger keys actions, otherwise it will only list information</td>
    </tr>
        </table>


Examples
--------

.. raw:: html

    <br/>


::

    - name: Add local key named my_key to mist.io
      mist_keys:
        mist_email: your@email.com
        mist_password: yourpassword
        name: myKey
        state: present
        key: /home/user/.ssh/my_key
    
    - name: Auto-generate key and save locally
      mist_keys:
        mist_email: your@email.com
        mist_password: yourpassword
        name: autoKey
        state: present
        auto_generate: true
        save_locally: true
        local_save_path: /path/to/save
    
    - name: Delete key named myKey
      mist_keys:
        mist_email: your@email.com
        mist_password: yourpassword
        name: myKey
        state: absent
    
    - name: List info for key named myKey
      mist_keys:
        mist_email: your@email.com
        mist_password: yourpassword
        name: myKey
      register: key
    

