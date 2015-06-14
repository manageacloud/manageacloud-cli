import unittest

import mock

import maccli.service.provider
from maccli.config import RELEASE_ANY
from mock_data import *


DEFAULT_CONFIGURATION = "cookbook_tag"
DEFAULT_PROVIDER = "manageacloud"
DEFAULT_LOCATION = "sfo1"
DEFAULT_RELEASE = RELEASE_ANY
RELEASE_AMAZON = "amazon"


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.dao.api_provider.get_locations')
    def testlist_locations(self, mock):
        mock.return_value = (200, MOCK_LOCATION_LIST_JSON)
        json_response = maccli.service.provider.list_locations(DEFAULT_CONFIGURATION, DEFAULT_PROVIDER, DEFAULT_RELEASE)
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_LOCATION_LIST_JSON)

    @mock.patch('maccli.dao.api_provider.get_locations')
    def testlist_locations(self, mock):
        mock.return_value = (200, MOCK_LOCATION_LIST_RELEASES_JSON)
        json_response = maccli.service.provider.list_locations(DEFAULT_CONFIGURATION, DEFAULT_PROVIDER, RELEASE_AMAZON)
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_LOCATION_LIST_RELEASES_AMAZON_JSON)


    @mock.patch('maccli.dao.api_provider.get_hardwares')
    def test_list_hardwares(self, mock):
        mock.return_value = (200, MOCK_HARDWARE_LIST_JSON)
        json_response = maccli.service.provider.list_hardwares(DEFAULT_PROVIDER, DEFAULT_LOCATION, DEFAULT_CONFIGURATION, DEFAULT_RELEASE)
        self.assertTrue(mock.called)
        self.assertEqual(json_response, MOCK_HARDWARE_LIST_JSON)
