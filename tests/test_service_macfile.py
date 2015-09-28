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
        #self.stdout = sys.stdout
        #sys.stdout = self.buf = StringIO.StringIO()

        if os.getcwd().endswith("/tests"):
            self.mock_path = "mock"
        else:
            self.mock_path = "tests/mock"

    def tearDown(self):
        #sys.stdout = self.stdout
        pass

    def test_open_file(self):
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures, _, _ = maccli.service.macfile.parse_macfile(contents)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_open_file_no_order(self):
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures, _, _ = maccli.service.macfile.parse_macfile(contents)
        self.assertNotEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_NO_ORDER_INF, default_flow_style=False))

    def test_no_roles(self):
        contents = maccli.service.macfile.load_macfile("%s/vpc.aws.macfile" % self.mock_path)
        root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(contents)
        self.assertEquals(yaml.dump(root, default_flow_style=False), yaml.dump({'version': '1.0', 'name': 'demo'}, default_flow_style=False))
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump([], default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(OrderedDict([('vpc_inf', OrderedDict([('resource', 'create_vpc')])), ('subnet_inf', OrderedDict([('resource', 'create_subnet')])), ('subnet_enable_public_ips_inf', OrderedDict([('resource', 'subnet_enable_public_ips')])), ('internet_gateway_inf', OrderedDict([('resource', 'create_internet_gateway')])), ('attach_internet_gateway_to_vpc', OrderedDict([('resource', 'attach_internet_gateway')])), ('attach_route_to_internet_gateway', OrderedDict([('resource', 'create_route')]))]), default_flow_style=False))
        self.assertEquals(yaml.dump(actions, default_flow_style=False), yaml.dump(OrderedDict([('get_route', OrderedDict([('bash', 'aws ec2 describe-route-tables --filters Name=vpc-id,Values=resource.vpc_inf.json.Vpc.VpcId --region us-east-1')]))]), default_flow_style=False))
        self.assertEquals(resources, OrderedDict([('create_vpc', OrderedDict([('create bash', 'aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1'), ('destroy bash', 'aws ec2 delete-vpc --vpc-id resource.vpc_inf.json.Vpc.VpcId --region us-east-1')])), ('create_subnet', OrderedDict([('create bash', 'aws ec2 create-subnet --vpc-id resource.vpc_inf.json.Vpc.VpcId --cidr-block 10.0.1.0/24 --region us-east-1'), ('destroy bash', 'aws ec2 delete-subnet --subnet-id resource.subnet_inf.json.Subnet.SubnetId --region us-east-1')])), ('subnet_enable_public_ips', OrderedDict([('create bash', 'aws ec2 modify-subnet-attribute --subnet-id resource.subnet_inf.json.Subnet.SubnetId --map-public-ip-on-launch --region us-east-1')])), ('create_internet_gateway', OrderedDict([('create bash', 'aws ec2 create-internet-gateway --region us-east-1'), ('destroy bash', 'aws ec2 delete-internet-gateway --internet-gateway-id resource.internet_gateway_inf.json.InternetGateway.InternetGatewayId --region us-east-1')])), ('attach_internet_gateway', OrderedDict([('create bash', 'aws ec2 attach-internet-gateway --internet-gateway-id resource.internet_gateway_inf.json.InternetGateway.InternetGatewayId --vpc-id resource.vpc_inf.json.Vpc.VpcId --region us-east-1'), ('destroy bash', 'aws ec2 detach-internet-gateway --internet-gateway-id resource.internet_gateway_inf.json.InternetGateway.InternetGatewayId --vpc-id resource.vpc_inf.json.Vpc.VpcId --region us-east-1')])), ('create_route', OrderedDict([('create bash', 'aws ec2 create-route --route-table-id action.get_route.json.RouteTables.0.RouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id resource.internet_gateway_inf.json.InternetGateway.InternetGatewayId --region us-east-1')]))]))

    def test_convert_args_to_yaml(self):
        yaml = maccli.service.macfile.convert_args_to_yaml(Mock_yaml_args())
        self.assertEqual(yaml, MOCK_MACFILE)

    def test_open_file_port(self):
        contents = maccli.service.macfile.load_macfile("%s/aws-medium-pgbench.macfile" % self.mock_path)
        root, roles, infrastructures, _, _ = maccli.service.macfile.parse_macfile(contents)
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_ROLE, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_AWS_INF, default_flow_style=False))

    def test_open_file_infrastructure(self):
        contents = maccli.service.macfile.load_macfile("%s/infrastructure.aws.macfile" % self.mock_path)
        root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(contents)

        self.assertEquals(yaml.dump(root, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_V2_EXPECTED_ROOT, default_flow_style=False))
        self.assertEquals(yaml.dump(roles, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES, default_flow_style=False))
        self.assertEquals(yaml.dump(infrastructures, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES, default_flow_style=False))
        self.assertEquals(yaml.dump(actions, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS, default_flow_style=False))
        self.assertEquals(resources, MOCK_PARSE_MACFILE_V2_EXPECTED_RESOURCES)
        #self.assertEquals(yaml.dump(resources, default_flow_style=False), yaml.dump(MOCK_PARSE_MACFILE_V2_EXPECTED_RESOURCES, default_flow_style=False))

    def test_parse_params_valid(self):
        raw_params = maccli.service.macfile.parse_params(MOCK_MACFILE_PARAMS, MACFILE_PARAMS_VALID)
        self.assertEqual(raw_params, MOCK_MACFILE_PARAMS_VALID)

    def test_parse_params_valid_2(self):
        raw_params = maccli.service.macfile.parse_params(MOCK_MACFILE_PARAMS_2, MACFILE_PARAMS_EMPTY)
        self.assertEqual(raw_params, MOCK_MACFILE_PARAMS_2)

    def test_parse_params_invalid(self):
        self.assertRaises(MacParseParamException, maccli.service.macfile.parse_params, MOCK_MACFILE_PARAMS, MACFILE_PARAMS_INVALID)

    def test_parse_params_missing(self):
        self.assertRaises(MacParseParamException, maccli.service.macfile.parse_params, MOCK_MACFILE_PARAMS, MACFILE_PARAMS_ONE_MISSING)

