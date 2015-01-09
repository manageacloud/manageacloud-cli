import unittest

import mock

from mock_data import *
import maccli.command_cli
import maccli.dao.api_instance


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.helper.http.send_request')
    def test_dao_instance_list_command(self, mock_get_instance_list):
        mock_get_instance_list.return_value = 200, MOCK_INSTANCE_LIST_JSON, MOCK_INSTANCE_LIST_JSON_RAW
        json = maccli.dao.api_instance.get_list()
        self.assertEqual(MOCK_INSTANCE_LIST_JSON, json)


    @mock.patch('maccli.service.instance.list_instances')
    def test_cli_command_instance_list(self, mock_list_instances):
        mock_list_instances.return_value = MOCK_INSTANCE_LIST_JSON
        maccli.command_cli.instance_list()

