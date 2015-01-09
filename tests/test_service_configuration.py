import unittest

import mock

import maccli.service.configuration
from mock_data import *


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.dao.api_configuration.get_user_configuration')
    def test_list_configurations(self, mock):
        mock.return_value = (200, MOCK_CONFIGURATION_LIST_JSON)
        json_response = maccli.service.configuration.list_configurations()
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_CONFIGURATION_LIST_JSON)

    @mock.patch('maccli.dao.api_configuration.search_public_configuration')
    def test_list_configurations(self, mock):
        mock.return_value = (200, MOCK_CONFIGURATION_SEARCH_JSON)
        json_response = maccli.service.configuration.search_configurations(None)
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_CONFIGURATION_SEARCH_JSON)
