mac
=====

Manageacloud command line interface.


Installing the CLI
------------------

NOTE: The alpha version is not released to the general public. The beta version will be announced in February 2015.

In order to install the Manageacloud CLI, you can use pip install:


    pip install mac


Now you can start using it:

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
