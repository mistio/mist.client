Run commands
************

With ``mist`` command line tool you can run a bash command in multiple tagged servers at once.
For example to run a command on all your dev servers::

    mist run --command "touch something" --tag dev

Output
::

    Found tagged machines
    Found key association for machine: atlanta

    Finished in machine: atlanta

