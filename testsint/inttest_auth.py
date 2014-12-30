import unittest

import service

import service.auth
from mock_data import *


class AuthIntTestCase(unittest.TestCase):
    def setUp(self):
        self.user = service.user
        self.apikey = service.apikey

    def tearDown(self):
        service.user = self.user
        service.apiKey = self.apikey

    def test_auth_authenticate(self):
        service.auth.authenticate(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(FAKE_USER, service.user)
        self.assertEqual(FAKE_APIKEY, service.apikey)
        self.tearDown()


