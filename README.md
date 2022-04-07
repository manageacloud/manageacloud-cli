# mac
Manageacloud is a flexible orchestration platform. It allows you to create, destroy and organise servers and infrastructures.

## Features
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

# Installation

## Command Line Interface


Install via PIP `pip install`. If you don't have `pip3` in your system,
and your system is based in Debian, install the package `python3-pip`

```sh
pip3 install mac
```

[//]: # ()
[//]: # (## Community version of Manageacloud Framework)

[//]: # ()
[//]: # (The community version of Manageacloud includes the server backend and the command line interface. )

[//]: # (Please [read here]&#40;https://manageacloud.com/docs/getting-started/install&#41; how to install it.)

# Examples

## Standalone applications

To create a new server and install apache for Ubuntu

```sh
mac instance create -b "apt-get update && apt-get install apache2 -y" -r ubuntu:trusty
```

To create a new server and install apache for CentOS

```sh
mac instance create -b "apt-get update && apt-get install apache2 -y" -r centos:7
```

## Infrastructures

You can learn more about how to orchestrate infrastructure using our [quickstart guide](https://manageacloud.com/quickstart)

The following example:
 - Creates an instance and a load balancer in AWS
 - Deploys an application and version *version_2*
 
```sh
mac -s infrastructure macfile https://goo.gl/ezRWx1 -p INF_VERSION=2 APP_BRANCH=version_2
```

