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

## Examples

Create two instances of [Demo Application](https://manageacloud.com/configuration/demo_application>) in Amazon Web Services and configure a load balancer.


```yaml

    mac: 0.9.1
    description: Two instances and a load balancer for AWS
    name: demo
    version: '1.0'

    roles:

      app:
        instance create:
          configuration: demo_application
          environment:
          - DB_IP: 127.0.0.1
          - APP_BRANCH: master

    actions:
       get_id:
          ssh: wget -q -O - http://169.254.169.254/latest/meta-data/instance-id

       get_availability_zone:
          ssh: wget -q -O - http://169.254.169.254/latest/meta-data/placement/availability-zone


    resources:

       build_lb:
          create bash:
            aws elb create-load-balancer
              --load-balancer-name my-load-balancer
              --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80
              --region infrastructure.app_inf.location
              --availability-zones role.app.get_availability_zone

       register_lb:
          create bash:
            aws elb register-instances-with-load-balancer
              --load-balancer-name my-load-balancer
              --instances role.app.get_id
              --region infrastructure.app_inf.location

    infrastructures:

      app_inf:
        name: app
        provider: amazon
        location: us-east-1
        hardware: t1.micro
        role: app
        amount: 2

      build_lb_inf:
        resource: build_lb

      register_lb_inf:
        resource: register_lb
```

Create an AMI from [Demo Application](https://manageacloud.com/configuration/demo_application>) in Amazon Web Services and an autoscaling group and a load balancer.

```yaml

    mac: 0.9.2
    description: Scaled and Load-Balanced Application
    name: demo
    version: '1.0'
    
    roles:
      app:
        instance create:
          # application configuration defined at https://manageacloud.com/configuration/demo_application
          configuration: demo_application
          environment:
          - DB_IP: 127.0.0.1
          - APP_BRANCH: master
    
    actions:
       # will be executed on the instances to fetch information
       get_id:
          ssh: wget -q -O - http://169.254.169.254/latest/meta-data/instance-id
    
       get_availability_zone:
          ssh: wget -q -O - http://169.254.169.254/latest/meta-data/placement/availability-zone
    
       get_security_groups:
          ssh: wget -q -O - http://169.254.169.254/latest/meta-data/security-groups
    
    resources:
       # resources creates configurations in the cloud.
       
       # creates load balancer
       build_lb:
          create bash:
            aws elb create-load-balancer
              --load-balancer-name my-load-balancer
              --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80
              --region infrastructure.image_base_inf.location
              --availability-zones role.app.get_availability_zone
    
        # creates AMI from the role 'app'
       create_image:
          create bash:
              aws ec2 create-image
                --instance-id infrastructure.image_base_inf.get_id
                --name DemoApplication3
                --description MyDemoApplication
                --region infrastructure.image_base_inf.location
    
       create_launch_configuration:
          create bash:
              aws autoscaling create-launch-configuration
                --launch-configuration-name my-lc
                --image-id resource.create_image_inf.json.ImageId
                --instance-type infrastructure.image_base_inf.hardware
                --security-groups role.app.get_security_groups
                --region infrastructure.image_base_inf.location
    
       create_autoscale_group:
          create bash:
              aws autoscaling create-auto-scaling-group
                --auto-scaling-group-name my-lb-asg
                --launch-configuration-name my-lc
                --availability-zones role.app.get_availability_zone
                --load-balancer-names my-load-balancer
                --max-size 5
                --min-size 1
                --desired-capacity 2
                --region infrastructure.image_base_inf.location
    
    infrastructures:  # infrastructures runs everything. The order is preserved.
    
      # create E2C instance using the configuration for role 'app'
      image_base_inf:
        name: app
        provider: amazon
        location: us-east-1
        hardware: t1.micro
        role: app
        amount: 1
    
      # create the load balancer
      build_lb_inf:
        resource: build_lb
    
      # create the AMI from the E2C instance created before
      create_image_inf:
        ready: role.app
        resource: create_image
    
      # create launch configuration
      create_launch_configuration_inf:
        resource: create_launch_configuration
    
      # create autoscale group
      create_autoscale_group_inf:
        resource: create_autoscale_group
```

Demo requirements:
 - Install and configure [aws cli](http://docs.aws.amazon.com/cli/latest/userguide/installing.html#install-with-pip>) and [mac cli](https://manageacloud.com/article/orchestration/cli/installation)
 - Deploy a production server at Amazon Web Services using [Manageacloud](https://manageacloud.com/login) (sign up takes 1 minute)
 - save the previous contents to a file called `infrastructure.macfile` and run the command `mac infrastructure macfile infrastructure.macfile`

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