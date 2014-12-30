import tempfile
import unittest
import ConfigParser
import mac

import os
import mock
from mock_data import *


class AuthIntTestCase(unittest.TestCase):

    def setUp(self):
        self.user = mac.user
        self.apikey = mac.apikey

    def tearDown(self):
        mac.user = self.user
        mac.apikey = mac.apikey

    def test_auth_authenticate(self):
        mac.auth.authenticate(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(FAKE_USER, mac.user)
        self.assertEqual(FAKE_APIKEY, mac.apikey)
        self.tearDown()


