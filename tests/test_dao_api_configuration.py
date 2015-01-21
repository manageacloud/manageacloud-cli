import unittest
import sys
import StringIO

import mock

from mock_data import *
import maccli.dao.api_configuration


DEFAULT_CONFIGURATION = "cookbook_tag"
DEFAULT_PROVIDER = "manageacloud"
DEFAULT_LOCATION = "sfo1"


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        #self.stdout = sys.stdout
        #sys.stdout = self.buf = StringIO.StringIO()
        pass

    def tearDown(self):
        #sys.stdout = self.stdout
        pass

    @mock.patch('maccli.helper.http.send_request')
    def test_search_no_params(self, mock):
        mock.return_value = (200, MOCK_CONFIGURATION_SEARCH_JSON, MOCK_CONFIGURATION_SEARCH_JSON_RAW)
        status_code, json_response = maccli.dao.api_configuration.search_public_configuration(None)
        mock.assert_called_once_with("GET", "/configuration/search")
        self.assertEqual(json_response, MOCK_CONFIGURATION_SEARCH_JSON)
        self.assertEqual(status_code, 200)

    @mock.patch('maccli.helper.http.send_request')
    def test_search_one_param(self, mock):
        keywords = ['one']
        mock.return_value = (200, MOCK_CONFIGURATION_SEARCH_JSON, MOCK_CONFIGURATION_SEARCH_JSON_RAW)
        status_code, json_response = maccli.dao.api_configuration.search_public_configuration(keywords)
        mock.assert_called_once_with("GET", "/configuration/search?keyword=one")
        self.assertEqual(json_response, MOCK_CONFIGURATION_SEARCH_JSON)
        self.assertEqual(status_code, 200)

    @mock.patch('maccli.helper.http.send_request')
    def test_search_several_param(self, mock):
        keywords = ['one', 'two']
        mock.return_value = (200, MOCK_CONFIGURATION_SEARCH_JSON, MOCK_CONFIGURATION_SEARCH_JSON_RAW)
        status_code, json_response = maccli.dao.api_configuration.search_public_configuration(keywords)
        mock.assert_called_once_with("GET", "/configuration/search?keyword=one&keyword=two")
        self.assertEqual(json_response, MOCK_CONFIGURATION_SEARCH_JSON)
        self.assertEqual(status_code, 200)