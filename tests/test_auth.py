import tempfile
import unittest
import ConfigParser
import os

import mock

import maccli.service.auth
import maccli.dao.api_auth
import maccli.helper.http
from mock_data import *
import maccli


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.user = maccli.user
        self.apikey = maccli.apikey

    def tearDown(self):
        maccli.user = self.user
        maccli.apiKey = self.apikey

    @mock.patch('maccli.dao.api_auth.get_auth')
    def test_auth_authenticate(self, mock_get_auth):
        mock_get_auth.return_value = (MOCK_USER, MOCK_APIKEY)
        user, apikey = maccli.service.auth.authenticate(MOCK_USER, MOCK_PASSWORD)
        self.assertEqual(MOCK_USER, user)
        self.assertEqual(MOCK_APIKEY, apikey)
        self.tearDown()


    def test_auth_load_from_file(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        with file as f:
            f.writelines(["[auth]\n", "user = %s\n" % MOCK_USER, "apikey = %s\n" % MOCK_APIKEY])
        user_read, apikey_read = maccli.dao.api_auth.load_from_file(file.name)
        self.assertEqual(user_read, MOCK_USER)
        self.assertEqual(apikey_read, MOCK_APIKEY)
        os.remove(file.name)

    @mock.patch.object(maccli.dao.api_auth.ConfigParser.ConfigParser, 'read', side_effect=ConfigParser.Error)
    def test_auth_load_from_file_with_exception(self, mock_read):
        user_read, apikey_read = maccli.dao.api_auth.load_from_file('abc')
        self.assertIsNone(user_read)
        self.assertIsNone(apikey_read)

    def test_auth_is_authenticated(self):
        maccli.user = MOCK_USER
        maccli.apikey = MOCK_APIKEY
        self.assertTrue(maccli.service.auth.is_authenticated())

        maccli.user = None
        maccli.apikey = MOCK_APIKEY
        self.assertFalse(maccli.service.auth.is_authenticated())

        maccli.user = MOCK_USER
        maccli.apikey = None
        self.assertFalse(maccli.service.auth.is_authenticated())

        maccli.user = None
        maccli.apikey = None
        self.assertFalse(maccli.service.auth.is_authenticated())


    def test_auth_logout(self):
        maccli.user = MOCK_USER
        maccli.apikey = MOCK_APIKEY
        maccli.service.auth.logout()
        self.assertIsNone(maccli.user)
        self.assertIsNone(maccli.apikey)


    def test_auth_get_auth_header(self):
        maccli.user = MOCK_USER
        maccli.apikey = MOCK_APIKEY
        self.assertEqual({'Authorization': 'ApiKey %s:%s' % (MOCK_USER, MOCK_APIKEY)},
                         maccli.helper.http.get_auth_header())

        maccli.user = None
        maccli.apikey = MOCK_APIKEY
        self.assertEqual({}, maccli.helper.http.get_auth_header())

        maccli.user = MOCK_USER
        maccli.apikey = None
        self.assertEqual({}, maccli.helper.http.get_auth_header())

        maccli.user = None
        maccli.apikey = None
        self.assertEqual({}, maccli.helper.http.get_auth_header())
