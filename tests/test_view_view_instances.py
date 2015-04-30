import unittest

import mock

import maccli.view.view_instance
from mock_data import *


INSTANCES_RAW=[{u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 89, u'ipv4': u'', u'type': u'testing', u'id': u'nnrtg49kji92rgl56288rl06ml', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 89, u'ipv4': u'', u'type': u'testing', u'id': u'm9jj37g32mqhb90ftmpqhl4mtc', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}]

class AuthTestCase(unittest.TestCase):

    def test_show_processing_instances(self):
        maccli.view.view_instance.show_processing_instances(INSTANCES_RAW)

