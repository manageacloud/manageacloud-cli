mac
=====

mac is a command line tool that allows to
  - bootstrap bash scripts when you are creating a new cloud server, allowing to hook configuration management systems like Puppet, Chef, Ansible and more
  - create cloud infrastructures in Amazon Web Services, Google Cloud Engine, Digital Ocean and Rackspace.
  - Manage servers and infrastructures


mac is very useful for a set of business cases such:
 - `Orchestration of geographically disperse infrastructures <https://manageacloud.com/case-study/geographically-disperse-infrastructures>`_
 - `Continuous Integration <https://manageacloud.com/case-study/continuous-integration>`_
 - `Disaster Recovery <https://manageacloud.com/case-study/disaster-recovery>`_
 - `Continuous Delivery: <https://manageacloud.com/case-study/continuous-delivery>`_
 - `Cloud benchmarking: <https://manageacloud.com/case-study/cloud-benchmark>`_
 - `A/B Testing <https://manageacloud.com/case-study/ab-testing>`_



Installing the CLI
------------------

An automatic installation can be performed with the following command:

.. sourcecode:: bash

    curl -sSL https://manageacloud.com/mac | bash

For a manual installation you can use ``pip install``:

.. sourcecode:: bash

    pip install mac --pre


Getting started with the CLI
----------------------------

Once is installed, you need to login. `Create an account <https://manageacloud.com/register>`_ (it takes 1 minute)
if you don't have one available.

.. sourcecode:: bash

    $ mac -h
    usage: mac [-h] [--version] [-v] [-q]
               {login,instance,configuration,infrastructure} ...

    Manageacloud.com CLI

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program\'s version number and exit
      -v, --verbose         Show verbose information
      -q, --quiet           Enable loggable output

    mac's CLI commands:
      {login,instance,configuration,infrastructure}
        login               Login into Manageacloud.com
        instance            Instance related operations
        configuration       Server configuration related operations
        infrastructure      Infrastructure operations


Actions
----------------------------



Documentation
-------------
Documentation is available at https://manageacloud.com/docs

