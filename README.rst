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

Install vis ``pip3 install``:

.. sourcecode:: bash

    pip3 install mac

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

