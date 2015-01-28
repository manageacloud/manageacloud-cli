mac
=====

NOTE: The alpha version is not released to the general public. The beta version will be announced in February 2015.

Manageacloud command line interface.


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
