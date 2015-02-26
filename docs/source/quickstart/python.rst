Quickstart
**********

Install mist using pip::

    pip install mist


Let's add our backends, for example an ec2 and an Openstack::

    mist add-backend --provider ec2 --region ec2_ap_northeast --name EC2 --ec2-api-key ALKI098IGGYUG --ec2-api-secret dioLKNlkhiu89oiukhj
    mist add-backend --provider openstack --name Openstack --openstack--username admin --openstack-tenant admin --openstack-password admin_pass --openstack-auth-url http://10.0.1:5000

We can now provision new machines just like that::

    mist create-machine --backend EC2 --name mongo.myserver --location_id 0 --size_id m1.small --image_id ami-d9134ed8
    mist create_machine --backend Openstack --name mongo2.myopenstackserver --location_id 0 --size_id 2 --image_id 9l98oiji-8uklhjh-234-23444

We can tag machines into groups::

    mist tag mongo.myserver --new-tag dev
    mist tag mongo2.myopenstackserver --new-tag dev

We can run batch commands to all machines in the dev group::

    mist run --command "apt-get update -y" --tag dev


And even enable monitoring with a single command::

    mist enable-monitoring mongo.myserver
