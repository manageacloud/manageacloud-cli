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
    def test_list_configurations_filter_ids(self, mock):
        SELECTED_INSTANCES = [{u'status': u'Ready', u'servername': u'mcp-prod-b55', u'lifespan': 0, u'ipv4': u'166.78.136.158', u'type': u'production', u'id': u'vcb553nb5p40km5tc1ofl1t0t8', u'metadata': {u'system': {u'infrastructure': {u'hardware': u'DFW/2', u'provider': u'rackspaceus', u'location': u'DFW', u'lifespan': -1, u'deployment': u'production'}, u'role': {u'environment': {u'PASSWORD': u'4br4c4d4br4yeh', u'VPN_SERVER': u'10.0.1.113', u'IP_RANGE': u'10.0.1.114-126'}, u'cookbook_tag': u'base_worker', u'block_tags': [u'meeou161t7i4uhtuj6i0utc7n']}}}}]
        mock.return_value = MOCK_INSTANCE_LARGE_LIST_JSON
        response = maccli.service.instance.list_instances(name_or_ids="vcb553nb5p40km5tc1ofl1t0t8")
        self.assertTrue(mock.called)
        self.assertEqual(response, SELECTED_INSTANCES)

    @mock.patch('maccli.dao.api_instance.get_list')
    def test_list_configurations_filter_ids(self, mock):
        SELECTED_INSTANCES = [{u'status': u'Ready', u'servername': u'mcp-prod-b55', u'lifespan': 0, u'ipv4': u'166.78.136.158', u'type': u'production', u'id': u'vcb553nb5p40km5tc1ofl1t0t8', u'metadata': {u'system': {u'infrastructure': {u'hardware': u'DFW/2', u'provider': u'rackspaceus', u'location': u'DFW', u'lifespan': -1, u'deployment': u'production'}, u'role': {u'environment': {u'PASSWORD': u'4br4c4d4br4yeh', u'VPN_SERVER': u'10.0.1.113', u'IP_RANGE': u'10.0.1.114-126'}, u'cookbook_tag': u'base_worker', u'block_tags': [u'meeou161t7i4uhtuj6i0utc7n']}}}}, {u'status': u'Ready', u'servername': u'mcp-prod-d8b', u'lifespan': 0, u'ipv4': u'162.209.99.168', u'type': u'production', u'id': u'2sh6jr9eb3gqgls3gasi7nb9q2', u'metadata': {u'system': {u'infrastructure': {u'hardware': u'IAD/2', u'provider': u'rackspaceus', u'location': u'IAD', u'lifespan': -1, u'deployment': u'production'}, u'role': {u'environment': {u'PASSWORD': u'4br4c4d4br4yeh', u'VPN_SERVER': u'10.0.1.145', u'IP_RANGE': u'10.0.1.146-158'}, u'cookbook_tag': u'base_worker', u'block_tags': [u'meeou161t7i4uhtuj6i0utc7n']}}}}]
        mock.return_value = MOCK_INSTANCE_LARGE_LIST_JSON
        response = maccli.service.instance.list_instances(name_or_ids=["vcb553nb5p40km5tc1ofl1t0t8", "2sh6jr9eb3gqgls3gasi7nb9q2"])
        self.assertTrue(mock.called)
        self.assertEqual(response, SELECTED_INSTANCES)


    @mock.patch('maccli.dao.api_instance.get_list')
    def test_list_by_infrastructure(self, mock):
        mock.return_value = MOCK_INSTANCE_LIST_INFRASTRUCTURE_RAW
        instances = maccli.service.instance.list_by_infrastructure('testing', '1.0')
        self.assertTrue(mock.called)
        self.assertEqual(instances, MOCK_INSTANCE_LIST_INFRASTRUCTURE_CLEAN)





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




