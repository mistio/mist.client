.. _mist_sizes:


mist_sizes - Lists all available machine sizes for a backend
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1

Synopsis
--------

.. versionadded:: 1.7.1

Returns a list of all available machine sizes for a given backend
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
    <td>backend</td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td>Can be either backend's id or name</td>
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
        <td>Url of the mist.io service. By default https://mist.io. But if you have a custom installation of mist.io you can provide the url here</td>
    </tr>
        </table>


Examples
--------

.. raw:: html

    <br/>


::

    - name: List sizes for a backend
      mist_sizes:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: DigitalOcean
      register: sizes
    

