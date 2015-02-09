Ansible modules
***************
Once you have installed the ``mist`` package you'll be able to use the mist ansible modules in your playbooks.
The easiest way to do so is to run the ``mistplay`` command, which is a wrapper of ``ansible-playbook``::

    mistplay main.yml

.. toctree::
   :maxdepth: 1

   mist_providers_module
   mist_backends_module
   mist_images_module
   mist_sizes_module
   mist_locations_module
   mist_keys_module
   mist_module