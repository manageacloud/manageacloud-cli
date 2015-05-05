import StringIO
import os
import unittest
import sys
import yaml


import mock

from mock_data import *
import maccli.service.macfile
from maccli.helper.exception import MacParseEnvException


class AuthTestCase(unittest.TestCase):


    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

        if os.getcwd().endswith("/tests"):
            self.mock_path = "mock"
        else:
            self.mock_path = "tests/mock"

    def tearDown(self):
        sys.stdout = self.stdout


    def test_open_file(self):
        root, roles, infrastructures = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_open_file_no_order(self):
        root, roles, infrastructures = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        self.assertNotEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_NO_ORDER_INF, default_flow_style=False))

    def convert_args_to_yaml(self):
        maccli.service.macfile.convert_args_to_yaml(Mock_yaml_args)
        self.assertEqual(self.stdout, MOCK_YAML)
