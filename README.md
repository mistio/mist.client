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

Backends/Providers
==================
You can see a list of all supported providers:

```
client.supported_providers

[{u'provider': u'bare_metal', u'title': u'Bare Metal Server'},
 {u'provider': u'ec2_ap_northeast', u'title': u'EC2 AP NORTHEAST'},
 {u'provider': u'ec2_ap_southeast', u'title': u'EC2 AP SOUTHEAST'},
 {u'provider': u'ec2_ap_southeast_2', u'title': u'EC2 AP Sydney'},
 {u'provider': u'ec2_eu_west', u'title': u'EC2 EU Ireland'},
 {u'provider': u'ec2_sa_east', u'title': u'EC2 SA EAST'},
 {u'provider': u'ec2_us_east', u'title': u'EC2 US EAST'},
 {u'provider': u'ec2_us_west', u'title': u'EC2 US WEST'},
 {u'provider': u'ec2_us_west_oregon', u'title': u'EC2 US WEST OREGON'},
 {u'provider': u'gce', u'title': u'Google Compute Engine'},
 {u'provider': u'nephoscale', u'title': u'NephoScale'},
 {u'provider': u'digitalocean', u'title': u'DigitalOcean'},
 {u'provider': u'linode', u'title': u'Linode'},
 {u'provider': u'openstack', u'title': u'OpenStack'},
 {u'provider': u'rackspace:dfw', u'title': u'Rackspace DFW'},
 {u'provider': u'rackspace:ord', u'title': u'Rackspace ORD'},
 {u'provider': u'rackspace:iad', u'title': u'Rackspace IAD'},
 {u'provider': u'rackspace:lon', u'title': u'Rackspace LON'},
 {u'provider': u'rackspace:syd', u'title': u'Rackspace AU'},
 {u'provider': u'rackspace:hkg', u'title': u'Rackspace HKG'},
 {u'provider': u'rackspace_first_gen:us', u'title': u'Rackspace US (OLD)'},
 {u'provider': u'rackspace_first_gen:uk', u'title': u'Rackspace UK (OLD)'},
 {u'provider': u'softlayer', u'title': u'SoftLayer'},
 {u'provider': u'hpcloud:region-a.geo-1',
  u'title': u'HP Helion Cloud - US West'},
 {u'provider': u'hpcloud:region-b.geo-1',
  u'title': u'HP Helion Cloud - US East'},
 {u'provider': u'docker', u'title': u'Docker'}]
```

You can see which backends you have added in the mist.io service:

```
client.backends

{u'Testeras': Backend => Testeras:D1g9abwqGUmQuZKGGBMfCgw8AUQ}
```

You can add a backend (e.g. ec2_ap_northeast):

```
client.add_backend(title="MyBackend", provider="ec2_ap_northeast", key="XXXXXXXXXXXXXXXXXX", secret="xxxxxxxxxxxxxxxxxxxxxxxxxxx")

```

