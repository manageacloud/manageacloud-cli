import StringIO
import os
import unittest
import sys
import yaml


import mock

from mock_data import *
import maccli.service.macfile
from maccli.helper.exception import MacParseEnvException, MacParseParamException


class MacfileServiceTestCase(unittest.TestCase):


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
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures = maccli.service.macfile.parse_macfile(contents)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_open_file_no_order(self):
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures = maccli.service.macfile.parse_macfile(contents)
        self.assertNotEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_NO_ORDER_INF, default_flow_style=False))

    def test_convert_args_to_yaml(self):
        yaml = maccli.service.macfile.convert_args_to_yaml(Mock_yaml_args())
        self.assertEqual(yaml, MOCK_MACFILE)

    def test_open_file_port(self):
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures = maccli.service.macfile.parse_macfile(contents)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_parse_params_valid(self):
        raw_params = maccli.service.macfile.parse_params(MOCK_MACFILE_PARAMS, MACFILE_PARAMS_VALID)
        self.assertEqual(raw_params, MOCK_MACFILE_PARAMS_VALID)

    def test_parse_params_invalid(self):
        self.assertRaises(MacParseParamException, maccli.service.macfile.parse_params, MOCK_MACFILE_PARAMS, MACFILE_PARAMS_INVALID)

    def test_parse_params_missing(self):
        self.assertRaises(MacParseParamException, maccli.service.macfile.parse_params, MOCK_MACFILE_PARAMS, MACFILE_PARAMS_ONE_MISSING)

