mac
====

Manageacloud is a flexible orchestration platform. It allows you to create, destroy and organise servers and infrastructures.

Fork me on `GitHub <https://github.com/manageacloud/manageacloud-cli>`_!

Features
--------
 - Orchestrate servers
 - Orchestrate production ready infrastructure (golden images, autoscaling groups, load balancers, etc)
 - Versioning servers and infrastructure
 - Empower Continuous Delivery
 - View who is the owner of the resources (servers and infrastructure)
 - Interact with your servers using a Command Line Interface, REST Api or Web Interface
 - Manage access to servers
 - Convert your infrastructure into code
 - Orchestrate servers using your existing automation codes (eg Docker, Puppet, Chef, SaltStack, etc)
 - Test server configurations easily
 - Integrate any technology that can be operated from the command line interface or an API
 - Keep the history (including logs) of servers and infrastructure
 - Trigger events via WebHooks
 - Although Manageacloud is technology agnostic, we have created some shortcuts for easier operation with Amazon Web Services, Google Compute Engine, Rackspace and Digital Ocean

Access to the `documentation <https://manageacloud.com/docs>`_ or to the `quickstart guide <https://manageacloud.com/quickstart>`_ to learn more.

Installation
============

Command Line Interface
----------------------

You can install the CLI and any required dependency by executing:

.. sourcecode:: bash

    curl -sSL https://manageacloud.com/mac | bash

You can also use ``pip install``:

.. sourcecode:: bash

    pip install mac

Community version of Manageacloud Framework
-------------------------------------------

The community version of Manageacloud includes the server backend and the command line interface.
Please `read here <https://manageacloud.com/docs/getting-started/install>`_ how to install it.


Examples
========

Standalone applications
-----------------------

To create a new server and install apache for Ubuntu

.. sourcecode:: bash

    mac instance create -b "apt-get update && apt-get install apache2 -y" -r ubuntu:trusty

To create a new server and install apache for CentOS

.. sourcecode:: bash

    mac instance create -b "apt-get update && apt-get install apache2 -y" -r centos:7


To install Wordpress

.. sourcecode:: bash

    mac instance create -c basic_wordpress_installation

Infrastructures
---------------

You can learn more about how to orchestrate infrastructure using our [quickstart guide](https://manageacloud.com/quickstart)

The following example:
 - Creates an instance and a load balancer in AWS
 - Deploys an application and version *version_2*

This infrastructure has a *name* and a *version*, which makes it ideal for some scenarios such as blue-green deployments.

.. sourcecode:: bash

    mac -s infrastructure macfile https://goo.gl/ezRWx1 -p INF_VERSION=2 APP_BRANCH=version_2



Build status
------------

|mac-1| `Wheezy 7 <https://manageacloud.com/configuration/mac/builds>`_

|mac-2| `Ubuntu Trusty Tahr 14.04 <https://manageacloud.com/configuration/mac/builds>`_

|mac-5| `CentOS 7 <https://manageacloud.com/configuration/mac/builds>`_

|mac-6| `Ubuntu Utopic Unicorn 14.10 <https://manageacloud.com/configuration/mac/builds>`_

|mac-7| `Debian Jessie 8 <https://manageacloud.com/configuration/mac/builds>`_

|mac-8| `Ubuntu Ubuntu Vivid Vervet 15.04 <https://manageacloud.com/configuration/mac/builds>`_

.. |mac-1| image:: https://manageacloud.com/configuration/mac/build/1/image
.. _mac-1: https://manageacloud.com/configuration/mac/builds
.. |mac-2| image:: https://manageacloud.com/configuration/mac/build/2/image
.. _mac-2: https://manageacloud.com/configuration/mac/builds
.. |mac-5| image:: https://manageacloud.com/configuration/mac/build/5/image
.. _mac-5: https://manageacloud.com/configuration/mac/builds
.. |mac-6| image:: https://manageacloud.com/configuration/mac/build/6/image
.. _mac-6: https://manageacloud.com/configuration/mac/builds
.. |mac-7| image:: https://manageacloud.com/configuration/mac/build/7/image
.. _mac-7: https://manageacloud.com/configuration/mac/builds
.. |mac-8| image:: https://manageacloud.com/configuration/mac/build/8/image
.. _mac-8: https://manageacloud.com/configuration/mac/builds