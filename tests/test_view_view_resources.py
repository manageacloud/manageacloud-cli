import unittest

import mock

import maccli.view.view_resource
from mock_data import *

RESOURCES_PROCESSED = [{'build_lb_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "DNSName": "my-load-balancer-1110685180.us-east-1.elb.amazonaws.com"\n}\n'}}, {'register_lb_inf': {'rc': 0, 'stderr': '', 'stdout': '{\n    "Instances": [\n        {\n            "InstanceId": "i-d3911600"\n        }\n    ]\n}\n'}}]

class ResourcesViewTestCase(unittest.TestCase):

    def test_show_resources(self):
        maccli.view.view_resource.show_resources(RESOURCES_PROCESSED)
