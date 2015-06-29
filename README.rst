mac
====

mac is a command line tool that allows to
  - bootstrap bash scripts when you are creating a new cloud server, allowing to hook configuration management systems like Puppet, Chef, Ansible and more
  - create cloud infrastructures in Amazon Web Services, Google Cloud Engine, Digital Ocean and Rackspace.
  - Manage servers and infrastructures


mac is very useful for a set of business cases such:
 - `Orchestration of geographically disperse infrastructures <https://manageacloud.com/case-study/geographically-disperse-infrastructures>`_
 - `Continuous Integration <https://manageacloud.com/case-study/continuous-integration>`_
 - `Disaster Recovery <https://manageacloud.com/case-study/disaster-recovery>`_
 - `Continuous Delivery <https://manageacloud.com/case-study/continuous-delivery>`_
 - `Cloud benchmarking <https://manageacloud.com/case-study/cloud-benchmark>`_
 - `A/B Testing <https//manageacloud.com/case-study/ab-testing>`_



Installing the CLI
------------------

An automatic installation can be performed with the following command:

.. sourcecode:: bash

    curl -sSL https://manageacloud.com/mac | bash

You can also use ``pip install``:

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

Documentation
-------------
Documentation is available at https://manageacloud.com/article/orchestration/cli

Build status
------------

|mac-1| Debian Wheezy 7

|mac-2| Ubuntu Trusty Tahr 14.04

|mac-3| CentOS 6.5

|mac-5| CentOS 7

|mac-6| Ubuntu Utopic Unicorn 14.10

|mac-7| Debian Jessie 8

|mac-8| Ubuntu Ubuntu Vivid Vervet 15.04

.. |mac-1| image:: https://manageacloud.com/configuration/mac/build/1/image
.. _mac-1: https://manageacloud.com/configuration/mac/builds
.. |mac-2| image:: https://manageacloud.com/configuration/mac/build/2/image
.. _mac-2: https://manageacloud.com/configuration/mac/builds
.. |mac-3| image:: https://manageacloud.com/configuration/mac/build/3/image
.. _mac-3: https://manageacloud.com/configuration/mac/builds
.. |mac-5| image:: https://manageacloud.com/configuration/mac/build/5/image
.. _mac-5: https://manageacloud.com/configuration/mac/builds
.. |mac-6| image:: https://manageacloud.com/configuration/mac/build/6/image
.. _mac-6: https://manageacloud.com/configuration/mac/builds
.. |mac-7| image:: https://manageacloud.com/configuration/mac/build/7/image
.. _mac-7: https://manageacloud.com/configuration/mac/builds
.. |mac-8| image:: https://manageacloud.com/configuration/mac/build/8/image
.. _mac-8: https://manageacloud.com/configuration/mac/builds