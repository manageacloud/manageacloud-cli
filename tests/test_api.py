import unittest

import mock

from mock_data import *
import dao.api_auth


class AuthTestCase(unittest.TestCase):
    @mock.patch('mac.http.send_request')
    def test_auth_authenticate_ok(self, mock_get_auth):
        mock_get_auth.return_value = 200, MOCK_LOGIN_JSON
        user, apiKey = dao.api_auth.get_auth(MOCK_USER, MOCK_PASSWORD)
        self.assertEqual(MOCK_USER, user)
        self.assertEqual(MOCK_APIKEY, apiKey)
