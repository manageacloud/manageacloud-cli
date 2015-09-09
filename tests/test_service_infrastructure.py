import unittest

import mock

import maccli.service.infrastructure
from mock_data import *

MOCK_INFRASTRUCTURE = [{u'cloudServers': [{u'status': u'Ready', u'servername': u'mct-lb-eh4', u'lifespan': 67, u'ipv4': u'130.211.132.25', u'type': u'testing', u'id': u'eh4gpld06l3itv18k3hvbnrumu', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'lb', u'environment_raw': [{u'APP_IP': u'app.PRIVATE_IP'}], u'version': u'2.0', u'name': u'demo', u'macfile_role_name': u'lb'}, u'system': {u'infrastructure': {u'hardware': u'https://www.googleapis.com/compute/v1/projects/manageacloud-instances/zones/REPLACE_ZONE/machineTypes/f1-micro', u'deployment': u'testing', u'location': u'us-central1-c', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'APP_IP': [u'10.240.229.100']}, u'cookbook_tag': u'loadbalancer', u'block_tags': [{}]}}}}], u'name': u'demo', u'versions': [u'2.0']}]
MOCK_INFRASTRUCTURE_300 = [{u'cloudServers': [{u'status': u'Ready', u'servername': u'mct-lb-eh4', u'lifespan': 300, u'ipv4': u'130.211.132.25', u'type': u'testing', u'id': u'eh4gpld06l3itv18k3hvbnrumu', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'lb', u'environment_raw': [{u'APP_IP': u'app.PRIVATE_IP'}], u'version': u'2.0', u'name': u'demo', u'macfile_role_name': u'lb'}, u'system': {u'infrastructure': {u'hardware': u'https://www.googleapis.com/compute/v1/projects/manageacloud-instances/zones/REPLACE_ZONE/machineTypes/f1-micro', u'deployment': u'testing', u'location': u'us-central1-c', u'lifespan': 300, u'provider': u'manageacloud'}, u'role': {u'environment': {u'APP_IP': [u'10.240.229.100']}, u'cookbook_tag': u'loadbalancer', u'block_tags': [{}]}}}}], u'name': u'demo', u'versions': [u'2.0']}]
MOCK_INSTANCE_300 = {u'status': u'Ready', u'servername': u'mct-lb-eh4', u'lifespan': 300, u'ipv4': u'130.211.132.25', u'type': u'testing', u'id': u'eh4gpld06l3itv18k3hvbnrumu', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'lb', u'environment_raw': [{u'APP_IP': u'app.PRIVATE_IP'}], u'version': u'2.0', u'name': u'demo', u'macfile_role_name': u'lb'}, u'system': {u'infrastructure': {u'hardware': u'https://www.googleapis.com/compute/v1/projects/manageacloud-instances/zones/REPLACE_ZONE/machineTypes/f1-micro', u'deployment': u'testing', u'location': u'us-central1-c', u'lifespan': 300, u'provider': u'manageacloud'}, u'role': {u'environment': {u'APP_IP': [u'10.240.229.100']}, u'cookbook_tag': u'loadbalancer', u'block_tags': [{}]}}}}
NAME = "demo"


class ServiceInfrastructureTestCase(unittest.TestCase):

    @mock.patch('maccli.dao.api_infrastructure.search_infrastructure')
    @mock.patch('maccli.dao.api_instance.update')
    def test_lifespan_name(self, mock_update, mock_search):
        mock_search.return_value = 200, MOCK_INFRASTRUCTURE
        mock_update.return_value = MOCK_INSTANCE_300
        json_response = maccli.service.infrastructure.lifespan(300, NAME, None)
        self.assertTrue(mock_update.called)
        self.assertEqual(json_response, MOCK_INFRASTRUCTURE_300)

