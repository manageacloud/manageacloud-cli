# mac
mac is a command line tool that allows to
 - bootstrap bash scripts when you are creating a new cloud server, allowing to hook configuration management systems like Puppet, Chef, Ansible and more
 - create cloud infrastructures in Amazon Web Services, Google Cloud Engine, Digital Ocean and Rackspace.
 - Manage servers and infrastructures


[Manageacloud](https://manageacloud.com) simplifies tasks such:
 - [Orchestration of infrastructures](https://manageacloud.com/case-study/geographically-disperse-infrastructures)
 - [Continuous Integration](https://manageacloud.com/case-study/continuous-integration)
 - [Continuous Development](https://manageacloud.com/case-study/disaster-recovery)
 - [Continuous Delivery](https://manageacloud.com/case-study/continuous-delivery)
 - [Cloud benchmarking](https://manageacloud.com/case-study/cloud-benchmark)
 - [A/B Testing](https//manageacloud.com/case-study/ab-testing)


## Installing the CLI

An automatic installation can be performed with the following command:

```sh
curl -sSL https://manageacloud.com/mac | bash
```

You can also use ``pip install``:
```sh
pip install mac --pre
```

## Getting started with the CLI


Once is installed, you need to login. [Create an account](https://manageacloud.com/register) (it takes 1 minute) if you don't have one available yet.

```sh

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
```

## Documentation
The documentation is available at the [official website](https://manageacloud.com/docs)

## Build status

Distribution  | Status
------------- | -------------
[Ubuntu Ubuntu Vivid Vervet 15.04](https://manageacloud.com/configuration/mac) | [![Ubuntu Ubuntu Vivid Vervet 15.04](https://manageacloud.com/configuration/mac/build/8/image)](https://manageacloud.com/configuration/mac/builds)
[CentOS 6.5](https://manageacloud.com/configuration/mac) | [![CentOS 6.5](https://manageacloud.com/configuration/mac/build/3/image)](https://manageacloud.com/configuration/mac/builds)
[Debian Wheezy 7.0](https://manageacloud.com/configuration/mac) | [![Debian Wheezy 7.0](https://manageacloud.com/configuration/mac/build/1/image)](https://manageacloud.com/configuration/mac/builds)
[Ubuntu Trusty Tahr 14.04](https://manageacloud.com/configuration/mac) | [![Ubuntu Trusty Tahr 14.04](https://manageacloud.com/configuration/mac/build/2/image)](https://manageacloud.com/configuration/mac/builds)
[Debian Jessie 8](https://manageacloud.com/configuration/mac) | [![Debian Jessie 8](https://manageacloud.com/configuration/mac/build/7/image)](https://manageacloud.com/configuration/mac/builds)
[CentOS 7](https://manageacloud.com/configuration/mac) | [![CentOS 7](https://manageacloud.com/configuration/mac/build/5/image)](https://manageacloud.com/configuration/mac/builds)
[Ubuntu Utopic Unicorn 14.10](https://manageacloud.com/configuration/mac) | [![Ubuntu Utopic Unicorn 14.10](https://manageacloud.com/configuration/mac/build/6/image)](https://manageacloud.com/configuration/mac/builds)