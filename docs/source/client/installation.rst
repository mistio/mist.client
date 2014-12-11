Installation
************

Install using pip
=================
This is the easiest way to obtain the mist package::

    pip install mist


Bash completion
===============
To enable bash completion, you have to do the following::

    sudo activate-global-python-argcomplete

If you are on Mac OSX, you have to do the following::

    activate-global-python-argcomplete --dest=/usr/local/opt/bash-completion/etc/bash_completion.d

And then add the following line in your ``~/.bashrc``::

    eval "$(register-python-argcomplete  /usr/bin/mist)"

If you are on Mac OSX, you have to add the following line to your ``~/.bash_profile``::

    eval "$(register-python-argcomplete  mist)"
