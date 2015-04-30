import unittest

import mock

from mock_data import *
import maccli.facade.macfile
from maccli.helper.exception import MacParseEnvException


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_private_ip_ok(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertTrue(processed)
        self.assertEqual(env_clean, {u'SHARED_MEMCACHE_IP': [u'172.31.36.70']})

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_private_ip_ko(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'no_match_shared_memcache', u'macfile_role_name': u'no_match_shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertFalse(processed)

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_public_ip_ok(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PUBLIC_IP'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertTrue(processed)
        self.assertEqual(env_clean, {u'SHARED_MEMCACHE_IP': [u'104.131.146.19']})

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_public_ip_ko(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PUBLIC_IP'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'no_match_shared_memcache', u'macfile_role_name': u'no_match_shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertFalse(processed)

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_facts_ok(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.FACT.lsbdistcodename'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertTrue(processed)
        self.assertEqual(env_clean, {u'SHARED_MEMCACHE_IP': [u'trusty']})

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_facts_ko(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.FACT.lsbdistcodename'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'no_match_shared_memcache', u'macfile_role_name': u'no_match_shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertFalse(processed)


    # @mock.patch('maccli.service.instance.facts')
    # def test_apply_infrastructure_changes_replace_private_ip_ok(self, mock_facts):
    #     mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
    #     INFRASTRUCTURE_INSTANCE_REPLACE = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}, {u'status': u'Instance completed', u'servername': u'mct-engine-ac4', u'lifespan': 85, u'ipv4': u'104.236.147.27', u'type': u'testing', u'id': u'20shqrf6pd66r76aue0qtdhh9f', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}, u'cookbook_tag': u'php_engine', u'block_tags': [u'9vouf1cm7l2biktjkd226763va']}}}}]
    #     maccli.facade.macfile.apply_infrastructure_changes(INFRASTRUCTURE_INSTANCE_REPLACE)
    #
    #
    # @mock.patch('maccli.service.instance.facts')
    # def test_apply_infrastructure_changes_replace_private_ip_fail(self, mock_facts):
    #     mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
    #     INFRASTRUCTURE_INSTANCE_REPLACE = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'unmatched_shared_memcache', u'macfile_role_name': u'unmatched_shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}, {u'status': u'Instance completed', u'servername': u'mct-engine-ac4', u'lifespan': 85, u'ipv4': u'104.236.147.27', u'type': u'testing', u'id': u'20shqrf6pd66r76aue0qtdhh9f', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}, u'cookbook_tag': u'php_engine', u'block_tags': [u'9vouf1cm7l2biktjkd226763va']}}}}]
    #     maccli.facade.macfile.apply_infrastructure_changes(INFRASTRUCTURE_INSTANCE_REPLACE)

