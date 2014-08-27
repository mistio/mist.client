import sys
import os
from git import Repo


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
        if package == "ansible":
            print "<ansible> package already installed"
    except ImportError:
        import pip
        print "Installing..."
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def init_playground(args, name):
    if args[-1] == "playground":
        print "You have to give a path for playground"
        sys.exit(1)
    else:
        install_and_import("choice")
        path = args[-1]
        if name:
            playground_dir = os.path.join(path, name)
        else:
            playground_dir = os.path.join(path, "Playground")

        confirm = choice.Binary('Init playground at path: %s' % playground_dir).ask()
        if confirm:
            if os.path.isdir(playground_dir):
                print "ERROR: %s already exists. Please delete before trying again" % playground_dir
                sys.exit(1)

            library_dir = os.path.join(playground_dir, "library")
            main_yaml_file_path = os.path.join(playground_dir, "main.yml")
            os.mkdir(playground_dir)
            os.mkdir(library_dir)
            main_yaml_file = """
            ---
            #Here goes the main playbook
            """
            with open(main_yaml_file_path, "w") as f:
                f.write(main_yaml_file)

            Repo.clone_from("git@github.com:mistio/mist.ansible.git", library_dir)
            sys.exit(0)
        else:
            sys.exit(0)


def ansible(args, name):
    if "install" in args:
        print ">>>Searching for <ansible> package"
        install_and_import("ansible")
        print
    elif "playground" in args:
        init_playground(args, name)