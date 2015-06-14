import unittest
import sys
import StringIO

import mock

from mock_data import *
import maccli.dao.api_provider


DEFAULT_CONFIGURATION = "cookbook_tag"
DEFAULT_RELEASE = "any"
DEFAULT_PROVIDER = "manageacloud"
DEFAULT_LOCATION = "sfo1"


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()
        # pass

    def tearDown(self):
        sys.stdout = self.stdout
        # pass

    @mock.patch('maccli.helper.http.send_request')
    def test_locations(self, mock):
        mock.return_value = (200, MOCK_LOCATION_LIST_JSON, MOCK_LOCATION_LIST_JSON_RAW)
        status_code, json_response = maccli.dao.api_provider.get_locations(DEFAULT_CONFIGURATION, DEFAULT_PROVIDER)
        mock.assert_called_once_with("GET", "/provider/locations?cookbook_tag=%s&provider=%s" % (
        DEFAULT_CONFIGURATION, DEFAULT_PROVIDER))
        self.assertEqual(json_response, MOCK_LOCATION_LIST_JSON)
        self.assertEqual(status_code, 200)

    @mock.patch('maccli.helper.http.send_request')
    def test_hardwares_ok(self, mock):
        mock.return_value = (200, MOCK_HARDWARE_LIST_JSON, MOCK_HARDWARE_LIST_JSON_RAW)
        status_code, json_response = maccli.dao.api_provider.get_hardwares(DEFAULT_PROVIDER, DEFAULT_LOCATION, DEFAULT_CONFIGURATION, DEFAULT_RELEASE)
        mock.assert_called_once_with("GET", "/provider/hardware?provider=%s&location=%s&release=%s&cookbook_tag=%s" % (
        DEFAULT_PROVIDER, DEFAULT_LOCATION, DEFAULT_RELEASE, DEFAULT_CONFIGURATION))
        self.assertEqual(json_response, MOCK_HARDWARE_LIST_JSON)
        self.assertEqual(status_code, 200)

    @mock.patch('maccli.helper.http.send_request')
    def test_hardwares_error(self, mock):
        mock.return_value = (400, None, "No credentials available")
        status_code, json_response = maccli.dao.api_provider.get_hardwares(DEFAULT_PROVIDER, DEFAULT_LOCATION, DEFAULT_CONFIGURATION, DEFAULT_RELEASE)
        mock.assert_called_once_with("GET", "/provider/hardware?provider=%s&location=%s&release=%s&cookbook_tag=%s" % (
        DEFAULT_PROVIDER, DEFAULT_LOCATION, DEFAULT_RELEASE, DEFAULT_CONFIGURATION))
        self.assertEqual(json_response, None)
        self.assertEqual(status_code, 400)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_HARDWARES_NO_CREDENTIALS.split()), ' '.join(out.split()))
