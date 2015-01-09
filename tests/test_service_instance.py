import unittest, sys, StringIO
import mock
import service.instance
from mock import mock_open
from mock_data import *

DEFAULT_SERVERNAME = "servername"
DEFAULT_SESSIONID = "sessionid"

class AuthTestCase(unittest.TestCase):

    @mock.patch('dao.api_instance.get_list')
    def test_list_configurations(self, mock):
        mock.return_value = MOCK_INSTANCE_LIST_JSON
        json_response = service.instance.list_instances()
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_INSTANCE_LIST_JSON)


    # @mock.patch('os.system')
    # @mock.patch('dao.api_instance.credentials')
    # def test_ssh_instance_privateKey(self, mock_credentials, mock_os):
    #     mock_credentials.return_value = MOCK_INSTANCE_CREDENTIALS_JSON
    #     service.instance.ssh_instance(DEFAULT_SERVERNAME, DEFAULT_SESSIONID)
    #     mock_os.assert_called_once_with("ssh root@104.236.164.139 -i /tmp/tmpfVO0A8")

    # @mock.patch('pexpect.spawn')
    # @mock.patch('dao.api_instance.credentials')
    # def test_ssh_instance_privateKey(self, mock_credentials, mock_os):
    #     mock_credentials.return_value = MOCK_INSTANCE_CREDENTIALS_PASS_JSON
    #     service.instance.ssh_instance(DEFAULT_SERVERNAME, DEFAULT_SESSIONID)
