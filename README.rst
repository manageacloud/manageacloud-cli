mac
=====

Manageacloud command line interface.

NOTE: This tool is pre-alpha and it is under heavy development. You can find more information at https://alpha.manageacloud.com


Installing the CLI
------------------

In order to install the Manageacloud CLI, you can use ``pip install``:

.. sourcecode:: bash

    pip install mac


Now you can start using it:

.. sourcecode:: bash

    mac -h

    usage: mac [-h] [--version] {login,instance,configuration} ...

    Manageacloud.com CLI

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

    mac's CLI commands:
      {login,instance,configuration}
        login               Login into Manageacloud.com
        instance            Manage testing or production server instances
        configuration       Manage configurations
