import unittest
import logging
import mock
from maccli.helper.exception import MacParameterNotFound

from mock_data import *
import maccli.helper.macfile


class HelperMacfileTestCase(unittest.TestCase):

    def test_has_dependencies_resources(self):
        command = "aws elb register-instances-with-load-balancer " \
               "--load-balancer-name my-load-balancer " \
               "--instances role.app.get_id infrastructure.app_inf.get_id"

        actual_dependencies = maccli.helper.macfile.has_dependencies(command, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES,
                                               MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
        self.assertTrue(actual_dependencies)

    def test_has_dependencies_resources_2(self):
        command = "aws autoscaling create-launch-configuration --launch-configuration-name my-lc --image-id resource.create_image_inf.json.ImageId"

        actual_dependencies = maccli.helper.macfile.has_dependencies(command, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES,
                                                                     MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
        self.assertTrue(actual_dependencies)

    def test_has_dependencies_infrastructure_params(self):
        command="aws elb create-load-balancer --load-balancer-name infrastructure.param.load-balancer-name --listeners infrastructure.listeners --security-groups sg-xxx --region us-east-1 --subnets subnet-yyy"
        INFRASTRUCTURES = OrderedDict([('build_lb_inf', OrderedDict([('resource', 'build_lb'), ('params', OrderedDict([('load-balancer-name', 'lb-local-parameters'), ('listerners', 'Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80')]))]))])
        actual_dependencies = maccli.helper.macfile.has_dependencies(command, [], INFRASTRUCTURES, [])
        self.assertTrue(actual_dependencies)

    def test_has_dependencies_infrastructures(self):
            #logging.basicConfig(level=logging.DEBUG)
            command = "aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region infrastructure.app_inf.location --availability-zones role.app.get_id.get_availability_zone"
            actual_dependencies = maccli.helper.macfile.has_dependencies(command, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES,
                                                                         MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
            self.assertTrue(actual_dependencies)

    def test_has_dependencies_action(self):
        ROLES=[]
        INFRASTRUCTURES=OrderedDict([('vpc_inf', OrderedDict([('resource', 'create_vpc')])), ('subnet_inf', OrderedDict([('resource', 'create_subnet')])), ('internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')])), ('attach_route_to_internet_gateway', OrderedDict([('resource', 'create_route')]))])
        ACTIONS=OrderedDict([('get_id', OrderedDict([('bash', 'aws ec2 describe-route-tables --filters "Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId" --region us-east-1')]))])
        command = "aws ec2 create-route --route-table-id action.json.RouteTableId --destination-cidr-block 0.0.0.0/0"
        actual_dependencies = maccli.helper.macfile.has_dependencies(command, ROLES, INFRASTRUCTURES, ACTIONS)
        self.assertTrue(actual_dependencies)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_resource(self, mock_run):
        CMD_RAW = 'aws elb register-instances-with-load-balancer --load-balancer-name my-load-balancer --instances role.app.get_id'
        CMD_CLEAN = 'aws elb register-instances-with-load-balancer --load-balancer-name my-load-balancer --instances i-3000b0e3'
        INSTANCES = [{u'status': u'Ready', u'servername': u'4oj-app-3000b0e3', u'lifespan': 3, u'ipv4': u'54.175.105.21', u'type': u'testing', u'id': u'44ojeae228l9d3aemcf4q2rcgk', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'app_inf', u'environment_raw': [{u'DB_IP': u'127.0.0.1'}, {u'APP_BRANCH': u'master'}], u'version': u'1.0', u'name': u'demo', u'macfile_role_name': u'app'}, u'system': {u'infrastructure': {u'hardware': u't1.micro', u'deployment': u'testing', u'location': u'us-east-1', u'lifespan': 60, u'provider': u'amazon'}, u'role': {u'environment': {u'APP_BRANCH': u'master', u'DB_IP': u'127.0.0.1'}, u'cookbook_tag': u'demo_application', u'block_tags': [{}]}}}}]
        mock_run.return_value = 0, "i-3000b0e3", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS, [])
        self.assertItemsEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_resource_no_instances(self, mock_run):
        CMD_RAW = 'aws elb register-instances-with-load-balancer --load-balancer-name my-load-balancer --instances role.app.get_id'
        INSTANCES = []
        mock_run.return_value = 0, "", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS, [])
        self.assertFalse(processed)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_infrastructure(self, mock_run):
        CMD_RAW = 'aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region infrastructure.app_inf.location --availability-zones role.app.get_availability_zone'
        CMD_CLEAN = 'aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region us-east-1 --availability-zones us-east-1e'
        INSTANCES = [{u'status': u'Ready', u'servername': u'4oj-app-3000b0e3', u'lifespan': 3, u'ipv4': u'54.175.105.21', u'type': u'testing', u'id': u'44ojeae228l9d3aemcf4q2rcgk', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'app_inf', u'environment_raw': [{u'DB_IP': u'127.0.0.1'}, {u'APP_BRANCH': u'master'}], u'version': u'1.0', u'name': u'demo', u'macfile_role_name': u'app'}, u'system': {u'infrastructure': {u'hardware': u't1.micro', u'deployment': u'testing', u'location': u'us-east-1', u'lifespan': 60, u'provider': u'amazon'}, u'role': {u'environment': {u'APP_BRANCH': u'master', u'DB_IP': u'127.0.0.1'}, u'cookbook_tag': u'demo_application', u'block_tags': [{}]}}}}]
        mock_run.return_value = 0, "us-east-1e", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_1_EXPECTED_ACTIONS, [])
        self.assertEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_infrastructure_resource_json(self, mock_run):
        CMD_RAW = "aws autoscaling create-launch-configuration --launch-configuration-name my-lc --image-id resource.create_image_inf.json.ImageId --instance-type m1.small"
        INSTANCES = [{u'status': u'Ready', u'servername': u's51-app-b16f8c19', u'lifespan': 33, u'ipv4': u'52.6.97.27', u'type': u'testing', u'id': u'ps511bs6t72qfr20r4toahq7i8', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'image_base_inf', u'environment_raw': [{u'DB_IP': u'127.0.0.1'}, {u'APP_BRANCH': u'master'}], u'version': u'1.0', u'name': u'demo', u'macfile_role_name': u'app'}, u'system': {u'infrastructure': {u'hardware': u't1.micro', u'deployment': u'testing', u'location': u'us-east-1', u'lifespan': 60, u'provider': u'amazon'}, u'role': {u'environment': {u'APP_BRANCH': u'master', u'DB_IP': u'127.0.0.1'}, u'cookbook_tag': u'demo_application', u'block_tags': [{}]}}}}]
        ROLES = OrderedDict([('app', OrderedDict([('instance create', OrderedDict([('configuration', 'demo_application'), ('environment', [OrderedDict([('DB_IP', '127.0.0.1')]), OrderedDict([('APP_BRANCH', 'master')])])]))]))])
        INFRASTRUCTURES = OrderedDict([('image_base_inf', OrderedDict([('name', 'app'), ('provider', 'amazon'), ('location', 'us-east-1'), ('hardware', 't1.micro'), ('role', 'app'), ('amount', 1)])), ('create_image_inf', OrderedDict([('resource', 'create_image')])), ('create_launch_configuration_inf', OrderedDict([('resource', 'create_launch_configuration')]))])
        ACTIONS = OrderedDict([('get_id', OrderedDict([('ssh', 'wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')]))])
        PROCESSED_RESOURCES = [{'create_image_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "ImageId": "ami-4d2dee26"\n}\n'}}]
        CMD_CLEAN = 'aws autoscaling create-launch-configuration --launch-configuration-name my-lc --image-id ami-4d2dee26 --instance-type m1.small'
        mock_run.return_value = 0, "i-b16f8c19", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)
        self.assertEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)

    def test_parse_env_multilevel_json(self):
        CMD_RAW = "aws ec2 create-subnet --vpc-id resource.vpc_inf.json.Vpc.VpcId --cidr-block 10.0.1.0/24 --region us-east-1"
        INSTANCES = []
        ROLES = []
        INFRASTRUCTURES = OrderedDict([('vpc_inf', OrderedDict([('resource', 'create_vpc')])), ('subnet_inf', OrderedDict([('resource', 'create_subnet')])), ('internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')])), ('attach_internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')]))])
        ACTIONS = OrderedDict([('get_id', OrderedDict([('bash', 'aws ec2 describe-route-tables --filters "Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId" --region us-east-1')]))])
        PROCESSED_RESOURCES = [{'vpc_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-7257a716", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}}]
        CMD_CLEAN = 'aws ec2 create-subnet --vpc-id vpc-7257a716 --cidr-block 10.0.1.0/24 --region us-east-1'
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)
        self.assertEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)

    @mock.patch('maccli.helper.cmd.run')
    def test_parse_action_json(self, mock_run):
        CMD_RAW = "aws ec2 create-route --route-table-id action.get_route.json.RouteTables.0.RouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id resource.internet_gateway_inf.json.InternetGateway.InternetGatewayId --region us-east-1"
        INSTANCES = []
        ROLES = []
        INFRASTRUCTURES = OrderedDict([('vpc_inf', OrderedDict([('resource', 'create_vpc')])), ('subnet_inf', OrderedDict([('resource', 'create_subnet')])), ('internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')])), ('attach_route_to_internet_gateway', OrderedDict([('resource', 'create_route')]))])
        ACTIONS = OrderedDict([('get_route', OrderedDict([('bash', 'aws ec2 describe-route-tables --filters "Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId" --region us-east-1')]))])
        PROCESSED_RESOURCES = [{'vpc_inf': {'cmd': 'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-ee45b58a", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}}, {'subnet_inf': {'cmd': u'aws ec2 create-subnet --vpc-id vpc-ee45b58a --cidr-block 10.0.1.0/24 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Subnet": {\n        "VpcId": "vpc-ee45b58a", \n        "CidrBlock": "10.0.1.0/24", \n        "State": "pending", \n        "AvailabilityZone": "us-east-1c", \n        "SubnetId": "subnet-97fcf9e0", \n        "AvailableIpAddressCount": 251\n    }\n}\n'}}, {'internet_gateway_inf': {'cmd': 'aws ec2 create-internet-gateway --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "InternetGateway": {\n        "Tags": [], \n        "InternetGatewayId": "igw-4b99bf2e", \n        "Attachments": []\n    }\n}\n'}}]
        CMD_CLEAN = 'aws ec2 create-route --route-table-id rtb-147bde70 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-4b99bf2e --region us-east-1'
        mock_run.return_value = 0, AWS_DESCRIBE_ROUTE_RAW, None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)
        self.assertEqual(CMD_CLEAN, actual)
        self.assertTrue(processed)

    def test_parse_parameter_not_found(self):
        CMD_RAW = "aws rds create-db-subnet-group --db-subnet-group-name mac-dev --db-subnet-group-description mac-dev --subnet-ids resource.subnet_2_inf.json.Subnet.SubnetId resource.subnet_inf.json.Subnet.SubnetId --region us-east-1"
        INSTANCES = []
        ROLES = []
        INFRASTRUCTURES = OrderedDict([('vpc_inf', OrderedDict([('resource', 'create_vpc')])), ('vpc_enable_hostname_dns_inf', OrderedDict([('resource', 'enable_hostname_resolution')])), ('subnet_inf', OrderedDict([('resource', 'create_subnet')])), ('subnet2_inf', OrderedDict([('resource', 'create_subnet_2')])), ('subnet_enable_public_ips_inf', OrderedDict([('resource', 'subnet_enable_public_ips')])), ('subnet_enable_public_ips_2_inf', OrderedDict([('resource', 'subnet_enable_public_ips_2')])), ('internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')])), ('attach_internet_gateway_to_vpc', OrderedDict([('resource', 'attach_internet_gateway')])), ('attach_route_to_internet_gateway', OrderedDict([('resource', 'create_route')])), ('authorize_ssh_inf', OrderedDict([('resource', 'authorize_ssh')])), ('create_rds_subnet_group_inf', OrderedDict([('resource', 'create_rds_subnet_group')])), ('create_rds_inf', OrderedDict([('resource', 'create_rds')]))])
        ACTIONS = OrderedDict([('get_route', OrderedDict([('bash', 'aws ec2 describe-route-tables --filters Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId --region us-east-1')])), ('get_security_group_id', OrderedDict([('bash', 'aws ec2 describe-security-groups --filters Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId --region us-east-1')]))])
        PROCESSED_RESOURCES = [{'vpc_inf': {'cmd': 'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-82e311e6", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}}, {'vpc_enable_hostname_dns_inf': {'cmd': u'aws ec2 modify-vpc-attribute --vpc-id vpc-82e311e6 --enable-dns-hostnames --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': ''}}, {'subnet_inf': {'cmd': u'aws ec2 create-subnet --vpc-id vpc-82e311e6 --cidr-block 10.0.1.0/24 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Subnet": {\n        "VpcId": "vpc-82e311e6", \n        "CidrBlock": "10.0.1.0/24", \n        "State": "pending", \n        "AvailabilityZone": "us-east-1b", \n        "SubnetId": "subnet-aa327081", \n        "AvailableIpAddressCount": 251\n    }\n}\n'}}, {'subnet2_inf': {'cmd': u'aws ec2 create-subnet --vpc-id vpc-82e311e6 --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Subnet": {\n        "VpcId": "vpc-82e311e6", \n        "CidrBlock": "10.0.2.0/24", \n        "State": "pending", \n        "AvailabilityZone": "us-east-1b", \n        "SubnetId": "subnet-a8327083", \n        "AvailableIpAddressCount": 251\n    }\n}\n'}}, {'subnet_enable_public_ips_inf': {'cmd': u'aws ec2 modify-subnet-attribute --subnet-id subnet-aa327081 --map-public-ip-on-launch --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': ''}}, {'subnet_enable_public_ips_2_inf': {'cmd': u'aws ec2 modify-subnet-attribute --subnet-id subnet-a8327083 --map-public-ip-on-launch --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': ''}}, {'internet_gateway_inf': {'cmd': 'aws ec2 create-internet-gateway --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "InternetGateway": {\n        "Tags": [], \n        "InternetGatewayId": "igw-d86141bd", \n        "Attachments": []\n    }\n}\n'}}, {'attach_internet_gateway_to_vpc': {'cmd': u'aws ec2 attach-internet-gateway --internet-gateway-id igw-d86141bd --vpc-id vpc-82e311e6 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': ''}}, {'attach_route_to_internet_gateway': {'cmd': u'aws ec2 create-route --route-table-id rtb-26d27542 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-d86141bd --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': '{\n    "Return": true\n}\n'}}, {'authorize_ssh_inf': {'cmd': u'aws ec2 authorize-security-group-ingress --group-id sg-e54b3d82 --protocol tcp --port 22 --cidr 0.0.0.0/0 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': ''}}]
        self.assertRaises(MacParameterNotFound, maccli.helper.macfile.parse_envs, CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)

    def test_parse_envs_destroy(self):
        CMD_RAW = "aws ec2 delete-vpc --vpc-id resource.vpc_inf.json.Vpc.VpcId"
        CMD_CLEAN = "aws ec2 delete-vpc --vpc-id vpc-b78c48d3"
        INSTANCES = []
        RESOURCES = [{u'create': {u'cmd': u'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1', u'rc': 0, u'stderr': u'', u'stdout': u'{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-b78c48d3", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}, u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'vpc_inf', u'version': u'1.0', u'name': u'demo', u'macfile_resource_name': u'create_vpc'}}, u'cmdDestroy': u'aws ec2 delete-vpc --vpc-id resource.vpc_inf.json.Vpc.VpcId', u'name': u'vpc_inf', u'cmdCreate': u'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1'}]
        actual = maccli.helper.macfile.parse_envs_destroy(CMD_RAW, INSTANCES, RESOURCES)
        self.assertEqual(CMD_CLEAN, actual)

    @mock.patch('maccli.helper.cmd.run')
    def test_parse_action_regex(self, mock_run):
        CMD_RAW = "command with parameter resource.bucket_inf.text.regex(s3://(.*)?/)"
        INSTANCES = []
        ROLES = []
        INFRASTRUCTURES = OrderedDict([('bucket_inf', OrderedDict([('resource', 'bucket')])), ('this_fails_inf', OrderedDict([('resource', 'this_fails')]))])
        ACTIONS = []
        PROCESSED_RESOURCES = [{'bucket_inf': {'cmd': 'aws s3 mb s3://s3-dev10 --region us-east-1', 'rc': 0, 'stderr': '', 'stdout': 'make_bucket: s3://s3-dev10/\n'}}]
        CMD_CLEAN = 'command with parameter s3-dev10'
        mock_run.return_value = 0, AWS_DESCRIBE_ROUTE_RAW, None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)
        self.assertEqual(CMD_CLEAN, actual)
        self.assertTrue(processed)

    @mock.patch('maccli.helper.cmd.run')
    def test_parse_resource_params(self, mock_run):
        CMD_RAW = "aws elb create-load-balancer --load-balancer-name infrastructure.param.load-balancer-name --listeners infrastructure.param.listeners --security-groups sg-xxx --region us-east-1 --subnets subnet-yyy"
        INSTANCES = []
        ROLES = []
        INFRASTRUCTURES = OrderedDict([('build_lb_inf', OrderedDict([('resource', 'build_lb'), ('params', OrderedDict([('load-balancer-name', 'lb-local-parameters'), ('listeners', 'Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80')]))]))])
        ACTIONS = []
        PROCESSED_RESOURCES = []
        INFRASTRUCTURE = INFRASTRUCTURES['build_lb_inf']
        CMD_CLEAN = 'aws elb create-load-balancer --load-balancer-name lb-local-parameters --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --security-groups sg-xxx --region us-east-1 --subnets subnet-yyy'
        mock_run.return_value = 0, AWS_DESCRIBE_ROUTE_RAW, None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES, INFRASTRUCTURE)
        self.assertEqual(CMD_CLEAN, actual)
        self.assertTrue(processed)


