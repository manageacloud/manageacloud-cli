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

    def test_show_resources_in_infrastructure_status(self):
        INFRASTRUCTURES_RESOURCES = [{u'cloudServers': [], u'name': u'demo', u'resources': [{u'create': {u'cmd': u'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1', u'rc': 0, u'stderr': u'', u'stdout': u'{\n    "Vpc": {\n        "InstanceTenancy": "default", \n        "State": "pending", \n        "VpcId": "vpc-b78c48d3", \n        "CidrBlock": "10.0.0.0/16", \n        "DhcpOptionsId": "dopt-838273e6"\n    }\n}\n'}, u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'vpc_inf', u'version': u'1.0', u'name': u'demo', u'macfile_resource_name': u'create_vpc'}}, u'cmdDestroy': u'aws ec2 delete-vpc --vpc-id resource.vpc_inf.json.Vpc.VpcId', u'name': u'vpc_inf', u'cmdCreate': u'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1'}], u'versions': [u'1.0']}]

        EXPECTED =  "+---------------------+---------+---------------+---------------+--------+\n"\
                    "| Infrastructure name | Version | Resource type | Resource name | Status |\n"\
                    "+---------------------+---------+---------------+---------------+--------+\n"\
                    "| demo                | 1.0     | create_vpc    | vpc_inf       | Ready  |\n"\
                    "+---------------------+---------+---------------+---------------+--------+\n"

        maccli.view.view_infrastructure.show_resources_in_infrastructure(INFRASTRUCTURES_RESOURCES)
        actual = self.bufout.getvalue()
        self.assertEqual(actual, EXPECTED)
