import StringIO
import unittest

import mock
import sys

import maccli.view.view_infrastructure
from mock_data import *

INFRASTRUCTURES = OrderedDict([('app_inf', OrderedDict([('name', 'app'), ('provider', 'amazon'), ('location', 'us-east-1'), ('hardware', 't1.micro'), ('role', 'app')])), ('build_lb_inf', OrderedDict([('resource', 'build_lb')])), ('register_lb_inf', OrderedDict([('resource', 'register_lb')]))])
RESOURCES_PROCESSED = [{'build_lb_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "DNSName": "my-load-balancer-1110685180.us-east-1.elb.amazonaws.com"\n}\n'}}, {'register_lb_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "Instances": [\n        {\n            "InstanceId": "i-d3911600"\n        }\n    ]\n}\n'}}]


class InfrastructureViewTestCase(unittest.TestCase):
    def setUp(self):
        self.stderr = sys.stderr
        self.stdout = sys.stdout
        sys.stderr = self.buf = StringIO.StringIO()
        sys.stdout = self.bufout = StringIO.StringIO()
        # pass

    def tearDown(self):
        sys.stderr = self.stderr
        sys.stdout = self.stdout
        # pass

    def test_show_resources_status(self):
        EXPECTED =  "+-----------------+---------+\n"\
                    "| Resource name   | Status  |\n"\
                    "+-----------------+---------+\n" \
                    "| app_inf         | Pending |\n" \
                    "| build_lb_inf    | OK      |\n"\
                    "| register_lb_inf | OK      |\n"\
                    "+-----------------+---------+\n"
        maccli.view.view_infrastructure.show_infrastructure_resources(INFRASTRUCTURES, RESOURCES_PROCESSED)
        actual = self.bufout.getvalue()
        self.assertEqual(actual, EXPECTED)