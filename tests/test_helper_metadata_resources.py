import unittest

import mock

import maccli.helper.metadata
from mock_data import *


class HelperMetadataTestCase(unittest.TestCase):

    def test_metadata(self):
        EXPECTED_META = {'macfile_infrastructure_name': 'consul01', 'macfile_role_name': 'consul', 'version': '1.0', 'environment_raw': [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])], 'name': 'consul'}
        macfile_root = {'version': '1.0', 'name': 'consul'}
        infrastructure_key = "consul01"
        role_key = "consul"
        role = OrderedDict([('branch', 'master'), ('configuration', 'consul')])
        infrastructure = OrderedDict([('deployment', 'testing'), ('location', 'us-central1-c'), ('name', 'consul01'), ('role', 'consul'), ('environment', [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])])])
        actual_meta = maccli.helper.metadata.metadata_instance(macfile_root, infrastructure_key, role_key, role, infrastructure)
        self.assertEqual(actual_meta, EXPECTED_META)

    def test_metadata_version_string(self):
        EXPECTED_META = {'macfile_infrastructure_name': 'consul01', 'macfile_role_name': 'consul', 'version': '1', 'environment_raw': [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])], 'name': 'consul'}
        macfile_root = {'version': 1, 'name': 'consul'}
        infrastructure_key = "consul01"
        role_key = "consul"
        role = OrderedDict([('branch', 'master'), ('configuration', 'consul')])
        infrastructure = OrderedDict([('deployment', 'testing'), ('location', 'us-central1-c'), ('name', 'consul01'), ('role', 'consul'), ('environment', [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')]), OrderedDict([('MEMBERS_IP', 'consul02.PRIVATE_IP')])])])
        actual_meta = maccli.helper.metadata.metadata_instance(macfile_root, infrastructure_key, role_key, role, infrastructure)
        self.assertEqual(actual_meta, EXPECTED_META)


    def test_get_environment(self):
        ROLE = OrderedDict([('branch', 'master'), ('configuration', 'consul'), ('environment', [OrderedDict([('MEMBERS_IP', 'consul.PRIVATE_IP')])])])
        INFRASTRUCTURE = OrderedDict([('deployment', 'testing'), ('location', 'us-central1-c'), ('name', 'consul01'), ('role', 'consul'), ('environment', [OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')])])])
        EXPECTED_ENVIRONMENT = [OrderedDict([('MEMBERS_IP', 'consul.PRIVATE_IP')]), OrderedDict([('MY_IP', 'consul01.PRIVATE_IP')])]
        actual_environment = maccli.helper.metadata.get_environment(ROLE, INFRASTRUCTURE)
        self.assertEqual(actual_environment, EXPECTED_ENVIRONMENT)

    def test_metadata_resource(self):
        EXPECTED_META = {'macfile_infrastructure_name': 'consul01', 'version': '1.0', 'name': 'consul', 'macfile_resource_name': 'resource_name_test'}
        macfile_root = {'version': '1.0', 'name': 'consul'}
        infrastructure_key = "consul01"
        resource_name = "resource_name_test"
        actual_meta = maccli.helper.metadata.metadata_resource(macfile_root, infrastructure_key, resource_name)
        self.assertEqual(actual_meta, EXPECTED_META)

    def test_metadata_resource_version_string(self):
        EXPECTED_META = {'macfile_infrastructure_name': 'consul01', 'version': '1', 'name': 'consul', 'macfile_resource_name': 'resource_name_test'}
        macfile_root = {'version': 1, 'name': 'consul'}
        infrastructure_key = "consul01"
        resource_name = "resource_name_test"
        actual_meta = maccli.helper.metadata.metadata_resource(macfile_root, infrastructure_key, resource_name)
        self.assertEqual(actual_meta, EXPECTED_META)
