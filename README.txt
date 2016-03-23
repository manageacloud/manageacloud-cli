mac
====

Manageacloud is a flexible orchestration platform. It allows you to create, destroy and organise servers and infrastructures.

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

Documentation: https://manageacloud.com/docs>
Quickstart guide: https://manageacloud.com/quickstart

Installation
============

Command Line Interface
----------------------

You can install the CLI and any required dependency by executing:

    curl -sSL https://manageacloud.com/mac | bash

You can also use ``pip install``:

    pip install mac --pre

Community version of Manageacloud Framework
-------------------------------------------

The community version of Manageacloud includes the server backend and the command line interface.
Please `read here <https://manageacloud.com/docs/getting-started/install>`_ how to install it.


Examples
========

Standalone applications
-----------------------

To create a new server and install apache for Ubuntu

    mac instance create -b "apt-get update && apt-get install apache2 -y" -r ubuntu:trusty

To create a new server and install apache for CentOS

    mac instance create -b "apt-get update && apt-get install apache2 -y" -r centos:7

To install Wordpress

    mac instance create -c basic_wordpress_installation

Infrastructures
---------------

You can learn more about how to orchestrate infrastructure using our quickstart guide ( https://manageacloud.com/quickstart )

The following example:
 - Creates an instance and a load balancer in AWS
 - Deploys an application and version *version_2*

This infrastructure has a *name* and a *version*, which makes it ideal for some scenarios such as blue-green deployments.

.. sourcecode:: bash

    mac -s infrastructure macfile https://goo.gl/ezRWx1 -p INF_VERSION=2 APP_BRANCH=version_2
