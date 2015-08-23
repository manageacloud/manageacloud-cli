import unittest
import logging
import mock

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

    def test_has_dependencies_infrastructures(self):
        #logging.basicConfig(level=logging.DEBUG)
        command = "aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region infrastructure.app_inf.location --availability-zones role.app.get_id.get_availability_zone"
        actual_dependencies = maccli.helper.macfile.has_dependencies(command, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES,
                                                                     MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
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
        ACTIONS = OrderedDict([('get_id', OrderedDict([('bash', 'ws ec2 describe-route-tables --filters "Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId" --region us-east-1')]))])
        PROCESSED_RESOURCES = [{'vpc_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-7257a716", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}}]
        CMD_CLEAN = 'aws ec2 create-subnet --vpc-id vpc-7257a716 --cidr-block 10.0.1.0/24 --region us-east-1'
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, ROLES, INFRASTRUCTURES, ACTIONS, PROCESSED_RESOURCES)
        self.assertEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)
