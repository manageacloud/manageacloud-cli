import unittest

import mock

import maccli.service.instance
from mock_data import *


DEFAULT_SERVERNAME = "servername"
DEFAULT_SESSIONID = "sessionid"

class AuthTestCase(unittest.TestCase):

    @mock.patch('maccli.dao.api_instance.get_list')
    def test_list_configurations(self, mock):
        mock.return_value = MOCK_INSTANCE_LIST_JSON
        json_response = maccli.service.instance.list_instances()
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_INSTANCE_LIST_JSON)

    @mock.patch('maccli.dao.api_instance.get_list')
    def test_list_by_infrastructure(self, mock):
        mock.return_value = MOCK_INSTANCE_LIST_INFRASTRUCTURE_RAW
        instances = maccli.service.instance.list_by_infrastructure('testing', '1.0')
        self.assertTrue(mock.called)
        self.assertEqual(instances, MOCK_INSTANCE_LIST_INFRASTRUCTURE_CLEAN)

    def test_metadata(self):
        EXPECTED_META = {'macfile_infrastructure_name': 'consul01', 'macfile_role_name': 'consul', 'version': '1.0', 'environment_raw': [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])], 'name': 'consul'}
        macfile_root = {'version': '1.0', 'name': 'consul'}
        infrastructure_key = "consul01"
        role_key = "consul"
        role = OrderedDict([('branch', 'master'), ('configuration', 'consul')])
        infrastructure = OrderedDict([('deployment', 'testing'), ('location', 'us-central1-c'), ('name', 'consul01'), ('role', 'consul'), ('environment', [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])])])
        actual_meta = maccli.service.instance.metadata(macfile_root, infrastructure_key, role_key, role, infrastructure)
        self.assertEqual(actual_meta, EXPECTED_META)

    def test_get_environment(self):
        ROLE = OrderedDict([('branch', 'master'), ('configuration', 'consul'), ('environment', [OrderedDict([('MEMBERS_IP', 'consul.PRIVATE_IP')])])])
        INFRASTRUCTURE = OrderedDict([('deployment', 'testing'), ('location', 'us-central1-c'), ('name', 'consul01'), ('role', 'consul'), ('environment', [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')])])])
        EXPECTED_ENVIRONMENT = [OrderedDict([('MEMBERS_IP', 'consul.PRIVATE_IP')]), OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')])]
        actual_environment = maccli.service.instance._get_environment(ROLE, INFRASTRUCTURE)
        self.assertEqual(actual_environment, EXPECTED_ENVIRONMENT)



# @mock.patch('os.system')
    # @mock.patch('maccli.dao.api_instance.credentials')
    # def test_ssh_instance_privateKey(self, mock_credentials, mock_os):
    #     mock_credentials.return_value = MOCK_INSTANCE_CREDENTIALS_PRIVKEY_JSON
    #     maccli.service.instance.ssh_instance(DEFAULT_SERVERNAME, DEFAULT_SESSIONID)
    #     mock_os.assert_called_once_with("ssh root@104.236.164.139 -i /tmp/tmpfVO0A8")

    # @mock.patch('pexpect.spawn')
    # @mock.patch('dao.api_instance.credentials')
    # def test_ssh_instance_privateKey(self, mock_credentials, mock_os):
    #     mock_credentials.return_value = MOCK_INSTANCE_CREDENTIALS_PASS_JSON
    #     service.instance.ssh_instance(DEFAULT_SERVERNAME, DEFAULT_SESSIONID)




