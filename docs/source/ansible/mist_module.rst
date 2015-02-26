.. _mist:


mist - Provision, monitor and manage machines with the mist.io service
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1

Synopsis
--------

.. versionadded:: 1.7.1

Manage machines in all of your added backends
You can add/remove multiple backends from multiple providers through mist.io service.
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
        <td>Can be either the backend's id or name</td>
    </tr>
            <tr>
    <td>image_extra</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Needed only when provisioning to Linode Provider</td>
    </tr>
            <tr>
    <td>image_id</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Id of the OS image you want to use to provision your machine</td>
    </tr>
            <tr>
    <td>key</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Name of the SSH-Key you want to associate with the machine. If <em>None</em>, the default SSH Key will be used</td>
    </tr>
            <tr>
    <td>location_id</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Id of the location/region you want to provision your machine to</td>
    </tr>
            <tr>
    <td>metric</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>It will be either the metric id for the supported metrics, or the name in case <em>python_file</em> is provided<em>wait_for_stats</em> needs to be true</td>
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
    <td>monitoring</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>If <em>True</em>, it will enable monitor to the machine</td>
    </tr>
            <tr>
    <td>name</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>The name you want the machine to have</td>
    </tr>
            <tr>
    <td>python_file</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>This is the path of a python file in case you want to add a custom python metric</td>
    </tr>
            <tr>
    <td>size_id</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>Id of the machine size you want to use</td>
    </tr>
            <tr>
    <td>state</td>
    <td>no</td>
    <td></td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td>If provided it will instruct the module to trigger machine actions, otherwise it will only list information</td>
    </tr>
            <tr>
    <td>unit</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>The unit of the metric you add. Can be left none</td>
    </tr>
            <tr>
    <td>value_type</td>
    <td>no</td>
    <td>gauge</td>
        <td><ul><li>gauge</li><li>derive</li></ul></td>
        <td>What type of value has the plugin</td>
    </tr>
            <tr>
    <td>wait</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>If <em>True</em>, the module will wait for the machine's SSH Daemon to be up and running and the SSH Key associated</td>
    </tr>
            <tr>
    <td>wait_for_stats</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>When enabling monitoring for the first time, it may take some time for the collectd agent to be installed.If <em>True</em>, it will wait for the monitoring stats to start</td>
    </tr>
            <tr>
    <td>wait_time</td>
    <td>no</td>
    <td>600</td>
        <td><ul></ul></td>
        <td>Time to wait when waiting for machine to be probed or monitor to be up and running</td>
    </tr>
        </table>


Examples
--------

.. raw:: html

    <br/>


::

    - name: Provision Ubuntu machine to EC2
      mist:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: EC2
        state: present
        name: MyMachine
        key: myKey
        image_id: ami-bddaa2bc
        size_id: m1.small
        location_id: 0
    
    - name: Provision SUSE machine on EC2 and enable monitoring
      mist:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: EC2
        state: present
        name: MyMachine
        key: myKey
        image_id: ami-9178e890
        size_id: m1.small
        location_id: 0
        monitoring: true
        wait_for_stats: true
    
    - name: List info for machine with name dbServer
      mist:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: EC2
        name: dbServer
      register: machine
    
    - name: Enable monitoring and add custom plugin.py
      mist:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: EC2
        name: dbServer
        state: present
        key: newKey
        wait: true
        monitoring: true
        wait_for_stats: true
        metric: MyPlugin
        python_file: /home/user/plugin.py

