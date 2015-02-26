.. _mist_providers:


mist_providers - Lists all available providers supported by the mist.io service
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1

Synopsis
--------

.. versionadded:: 1.7.1

Returns a list of all available providers and the corresponding regions that you can add and control through mist.io service.
*mist_email* and *mist_password* can be skipped if *~/.mist* config file is present.
See documentation for config file http://mist.readthedocs.org/en/latest/cmd/cmd.html

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
            <tr>
    <td>provider</td>
    <td>no</td>
    <td>all</td>
        <td><ul><li>ec2</li><li>rackspace</li><li>bare_metal</li><li>gce</li><li>openstack</li><li>linode</li><li>nephoscale</li><li>digitalocean</li><li>docker</li><li>hpcloud</li><li>softlayer</li><li>azure</li><li>libvirt</li><li>vcloud</li><li>indonesian_vcloud</li><li>all</li></ul></td>
        <td>By default <em>all</em>, which returns all supported providers by the mist.io service.You can explicitly set it to one of the choices to see only this provider-specific information</td>
    </tr>
        </table>


Examples
--------

.. raw:: html

    <br/>


::

    - name: List supported providers, simple case
      mist_providers:
        mist_email: your@email.com
        mist_password: yourpassword
        provider: all
      register: providers
    
    - name: List supported provider having ~/.mist config file present
      mist_providers:
        provider: all
      register: providers
    
    - name: List only ec2 provider options
      mist_providers:
        mist_email: your@email.com
        mist_password: yourpassword
        provider: ec2
      register: providers

