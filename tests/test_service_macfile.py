import os
import unittest
import yaml


import mock

from mock_data import *
import maccli.service.macfile
from maccli.helper.exception import MacParseEnvException


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        if os.getcwd().endswith("/tests"):
            self.mock_path = "mock"
        else:
            self.mock_path = "tests/mock"

    def test_open_file(self):

        roles, infrastructures = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_open_file_no_order(self):
        roles, infrastructures = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        self.assertNotEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_NO_ORDER_INF, default_flow_style=False))
