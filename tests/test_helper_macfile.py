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
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
        self.assertItemsEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_resource_no_instances(self, mock_run):
        CMD_RAW = 'aws elb register-instances-with-load-balancer --load-balancer-name my-load-balancer --instances role.app.get_id'
        INSTANCES = []
        mock_run.return_value = 0, "", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS)
        self.assertFalse(processed)

    @mock.patch('maccli.service.instance.ssh_command_instance')
    def test_parse_env_infrastructure(self, mock_run):
        CMD_RAW = 'aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region infrastructure.app_inf.location --availability-zones role.app.get_availability_zone'
        CMD_CLEAN = 'aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region us-east-1 --availability-zones us-east-1e'
        INSTANCES = [{u'status': u'Ready', u'servername': u'4oj-app-3000b0e3', u'lifespan': 3, u'ipv4': u'54.175.105.21', u'type': u'testing', u'id': u'44ojeae228l9d3aemcf4q2rcgk', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'app_inf', u'environment_raw': [{u'DB_IP': u'127.0.0.1'}, {u'APP_BRANCH': u'master'}], u'version': u'1.0', u'name': u'demo', u'macfile_role_name': u'app'}, u'system': {u'infrastructure': {u'hardware': u't1.micro', u'deployment': u'testing', u'location': u'us-east-1', u'lifespan': 60, u'provider': u'amazon'}, u'role': {u'environment': {u'APP_BRANCH': u'master', u'DB_IP': u'127.0.0.1'}, u'cookbook_tag': u'demo_application', u'block_tags': [{}]}}}}]
        mock_run.return_value = 0, "us-east-1e", None
        actual, processed = maccli.helper.macfile.parse_envs(CMD_RAW, INSTANCES, MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, MOCK_PARSE_MACFILE_V2_1_EXPECTED_ACTIONS)
        self.assertEqual(actual, CMD_CLEAN)
        self.assertTrue(processed)