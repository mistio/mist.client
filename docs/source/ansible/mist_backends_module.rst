.. _mist_backends:


mist_backends - Manage backends in the mist.io service
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1

Synopsis
--------

.. versionadded:: 1.7.1

Manage multi-cloud backends through mist.io service.
You can add/remove multiple backends from multiple providers through mist.io service.
Before you can provision, monitor etc machines through mist.io, you have to first add a backend to the mist.io service.
Mist.io supports
EC2,
Rackspace,
Openstack,
Linode,
Google Compute Engine,
SoftLayer,
Digital Ocean,
Nephoscale,
Bare metal servers,
Docker containers,
HP Cloud,
Azure,
VmWare - Vcloud,
KV``libvirt``,
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
    <td></td>
        <td><ul></ul></td>
        <td>Provider id for the backend you want to add to mist.io. You can see all the providers ids using the <span class='module'>mist_providers</span> module.</td>
    </tr>
            <tr>
    <td>state</td>
    <td>no</td>
    <td></td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td>If provided it will instruct the module to trigger backend actions, otherwise it will only list information</td>
    </tr>
            <tr>
    <td>title</td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td>The title you want the backend to have</td>
    </tr>
        </table>


Examples
--------

.. raw:: html

    <br/>


::

    - name: Add EC2 backend
      mist_backends:
        title: MyEC2
        provider: ec2
        api_key: kjhf98y9lkj0909kj90edffwwf432fd
        api_secret: LKHLKjlkdlkho8976dhjkjhd987987
        region: ec2_ap_northeast
        state: present
    
    - name: Add Rackspace backend
      mist_backends:
        title: MyRackspace
        provider: rackspace
        region: dfw
        username: rack_username
        api_key: sadlkjnjkhbi0HBCG
        state: present
    
    - name: Add Nephoscale backend
      mist_backends:
        title: MyNepho
        provider: nephoscale
        username: nepho_user
        password: nepho_pass
        state: present
    
    - name: Add SoftLayer backend
      mist_backends:
        title: MySoftLayer
        provider: softlayer
        username: SL09890
        api_key: kjhdskjhad987987098sdlkhjlajslkj
        state: present
    
    - name: Add Digital Ocena backend
      mist_backends:
        title: MyDigi
        provider: digitalocean
        token: oiulksdjkjhd0987098lkahkjdhkj....
        state: present
    
    - name: Add Google Compute Engine backend
      mist_backends:
        title: GCE
        provider: gce
        email: my.gce.email@gce
        project_id: electron-25
        private_key: /path/to/locally/stored/private_key
        state: present
    
    - name: Add Azure backend
      mist_backends:
        title: AZURE
        provider: azure
        subscription_id: lkjafh-08jhkl-09kljlj...
        certificate: /path/to/locally/saved/certificate
        state: present
    
    - name: Add Linode backend
      mist_backends:
        title: MyLinode
        provider: linode
        api_key: dlkjdljkd0989yKGFgjgc86798ohkl
        state: present
    
    - name: Add Bare Metal (or any server with ssh access)
      mist_backends:
        title: MyOtherServer
        provider: bare_metal
        machine_ip: 190.20.10.45
        machine_user: myuser
        machine_key: name_of_key_added_to_mist.io
        machine_port: 22
        state: present
    
    - name: Add vCloud backend
      mist_backends:
        title: MyVCLOUD
        provider: vcloud
        username: vuser
        password: vpass
        organization: Mist.io
        host: compute.idcloudonline.com
        state: present
    
    - name: Add Indonesian vCloud backend
      mist_backends:
        title: IndoVCLOUD
        provider: indonesian_vcloud
        username: vuser
        password: vpass
        organization: Mist.io
        state: present
    
    - name: Add KVM(libvirt) backend
      mist_backends:
        title: MyKVM
        provider: libvirt
        machine_hostname: 190.198.23.0
        machine_user: root
        machine_key: name_of_key_added_to_mist.io
        state: present
    
    - name: Add HP Cloud backend
      mist_backends:
        title: MyHP
        provider: hpcloud
        region: region-a.geo-1
        username: hpuser
        password: hppass
        tenant_name: my_tenant
        state: present
    
    - name: Add Openstack backend
      mist_backends:
        title: MyOPENSTACK
        provider: openstack
        username: user
        password: pass
        tenant_name: admin
        auth_url: http://190.132.20.22:5000
        region: my_region_if_exists
        state: present
    
    - name: Add Docker backend
      mist_backends:
        title: MyDOCKER
        provider: docker
        docker_host: 190.189.1.2
        docker_port: 4243
        auth_user: user if I have Basic HTTP AUTH setup
        auth_password: pass if I have Basic HTTP AUTH setup
        key_file: path to key file if I have TLS setup
        cert_file: path to cert file if I have TLS setup
    
    - name: List information about DigitalOcean backend
      mist_backends:
        mist_email: your@email.com
        mist_password: yourpassword
        backend: DigitalOcean
      register: backend

