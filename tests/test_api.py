import unittest
import subprocess

import mock

from mock_data import *
import maccli.dao.api_auth


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.helper.http.send_request')
    def test_auth_authenticate_ok(self, mock_get_auth):
        mock_get_auth.return_value = 200, MOCK_LOGIN_JSON, MOCK_LOGIN_JSON_RAW
        user, apiKey = maccli.dao.api_auth.get_auth(MOCK_USER, MOCK_PASSWORD)
        self.assertEqual(MOCK_USER, user)
        self.assertEqual(MOCK_APIKEY, apiKey)
