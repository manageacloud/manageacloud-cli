import unittest

import mock

import maccli.service.resource
from maccli.config import RELEASE_ANY
from mock_data import *


DEFAULT_RESOURCE = {u'name': u'load balancer 01', u'create': {u'cmd': u'aws elb create-load-balancer --load-balancer-name infrastructure.param.name --listeners infrastructure.param.listeners --availability-zones infrastructure.param.availability-zones', u'rc': 0, u'stderr': u'', u'stdout': u'{\n    "DNSName": "my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com"\n}\n'}, u'destroy': {u'rc': 0}, u'cmdDestroy': u'aws elb delete-load-balancer --load-balancer-name infrastructure.param.name --region us-east-1', u'cmdCreate': u'aws elb create-load-balancer --load-balancer-name infrastructure.param.name --listeners infrastructure.param.listeners --availability-zones infrastructure.param.availability-zones', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'load balancer 01', u'macfile_infrastructure_params': {u'listeners': u'Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80', u'region': u'us-east-1', u'name': u'my-demo-load-balancer', u'availability-zones': u'us-east-1b us-east-1c us-east-1d us-east-1e'}, u'version': u'1.0', u'name': u'demo', u'macfile_resource_name': u'elastic_load_balancer'}}}


class ResourceTestCase(unittest.TestCase):

    @mock.patch('maccli.dao.api_resource.get')
    def test_resource_get_text_regex(self, mock):
        mock.return_value = DEFAULT_RESOURCE
        clean = [u'{', u'', u'    "DNSName": "my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com\"', u'', u'}', u'']
        response = maccli.service.resource.get_resource_value("demo", "1.0", "load balancer 01", "text.regex(.*)")
        self.assertEqual(response, clean)

    @mock.patch('maccli.dao.api_resource.get')
    def test_resource_get_text_regex_position(self, mock):
        mock.return_value = DEFAULT_RESOURCE
        clean = '    "DNSName": "my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com"'
        response = maccli.service.resource.get_resource_value("demo", "1.0", "load balancer 01", "text.regex(.*)[2]")
        self.assertEqual(response, clean)

    @mock.patch('maccli.dao.api_resource.get')
    def test_resource_get_json(self, mock):
        mock.return_value = DEFAULT_RESOURCE
        clean = 'my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com'
        response = maccli.service.resource.get_resource_value("demo", "1.0", "load balancer 01", "json.DNSName")
        self.assertEqual(response, clean)

    @mock.patch('maccli.dao.api_resource.get')
    def test_resource_get_text(self, mock):
        mock.return_value = DEFAULT_RESOURCE
        clean = '{\n    "DNSName": "my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com"\n}\n'
        response = maccli.service.resource.get_resource_value("demo", "1.0", "load balancer 01", "text")
        self.assertEqual(response, clean)

    @mock.patch('maccli.dao.api_resource.get')
    def test_resource_get_none(self, mock):
        mock.return_value = DEFAULT_RESOURCE
        clean = '{\n    "DNSName": "my-demo-load-balancer-1589716593.us-east-1.elb.amazonaws.com"\n}\n'
        response = maccli.service.resource.get_resource_value("demo", "1.0", "load balancer 01", None)
        self.assertEqual(response, clean)

