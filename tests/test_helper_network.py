import unittest

from mock_data import *
import maccli.helper.network


class AuthTestCase(unittest.TestCase):
    def test_network(self):
        self.assertTrue(maccli.helper.network.is_ip_private("127.0.0.1"))
        self.assertTrue(maccli.helper.network.is_ip_private("192.168.0.1"))
        self.assertFalse(maccli.helper.network.is_ip_private("162.243.152.74"))
        self.assertTrue(maccli.helper.network.is_ip_private("10.10.10.10"))
        self.assertFalse(maccli.helper.network.is_ip_private("172.2.1.2"))
        self.assertTrue(maccli.helper.network.is_ip_private("172.16.1.2"))
        self.assertTrue(maccli.helper.network.is_ip_private("172.30.1.2"))
        self.assertTrue(maccli.helper.network.is_ip_private("172.31.1.2"))
        self.assertTrue(maccli.helper.network.is_ip_private("172.31.36.70"))
        self.assertFalse(maccli.helper.network.is_ip_private("172.32.1.2"))

    def test_local_loop(self):
        self.assertTrue(maccli.helper.network.is_local("127.0.0.1"))
        self.assertFalse(maccli.helper.network.is_local("192.168.0.1"))
        self.assertFalse(maccli.helper.network.is_local("162.243.152.74"))
        self.assertFalse(maccli.helper.network.is_local("10.10.10.10"))
        self.assertFalse(maccli.helper.network.is_local("172.2.1.2"))
        self.assertFalse(maccli.helper.network.is_local("172.16.1.2"))
        self.assertFalse(maccli.helper.network.is_local("172.30.1.2"))
        self.assertFalse(maccli.helper.network.is_local("172.31.1.2"))
        self.assertFalse(maccli.helper.network.is_local("172.32.1.2"))
