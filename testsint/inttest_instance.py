import unittest

import service

import service.instance


class AuthIntTestCase(unittest.TestCase):
    def test_instance_collection(self):
        service.instance.list_instances()
        # self.assertEqual(FAKE_USER, service.user)
        #self.assertEqual(FAKE_APIKEY, service.apikey)
        #self.tearDown()


