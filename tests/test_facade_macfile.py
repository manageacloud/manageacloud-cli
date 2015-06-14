import unittest
import sys
import StringIO

import mock
from maccli.config import MACFILE_ON_FAILURE_DESTROY_ALL, MACFILE_ON_FAILURE_DESTROY_OTHERS

from mock_data import *
import maccli.facade.macfile
from maccli.helper.exception import MacParseEnvException


class TestFacadeMacfileTestCase(unittest.TestCase):
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

    def test_parse_env_ok(self):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'127.0.0.1'}]
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, [])
        self.assertTrue(processed)
        self.assertEqual(env_clean, {u'SHARED_MEMCACHE_IP': u'127.0.0.1'})

    @mock.patch('maccli.service.instance.facts')
    def test_parse_env_facts_ko(self, mock_facts):
        ENV_RAWS = [{u'SHARED_MEMCACHE_IP': u'shared_memcache.FACT.lsbdistcodename'}]
        OTHER_INSTANCES = [{u'status': u'Ready', u'servername': u'mct-memcache-ea8', u'lifespan': 85, u'ipv4': u'104.131.146.19', u'type': u'testing', u'id': u'bo0h93s8t7vmqns1rbe4f6ujkb', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'no_match_shared_memcache', u'macfile_role_name': u'no_match_shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'provider': u'manageacloud', u'location': u'sfo1', u'lifespan': 90, u'deployment': u'testing'}, u'role': {u'cookbook_tag': u'eh_memcache', u'block_tags': [{}]}}}}]
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        env_clean, processed = maccli.facade.macfile.parse_instance_envs(ENV_RAWS, OTHER_INSTANCES)
        self.assertFalse(processed)

    def test_clean_up_ok(self):
        failed =  maccli.facade.macfile.clean_up(MOCK_RESPONSE_INSTANCE_LIST_JSON, None)
        self.assertFalse(failed)

    @mock.patch('maccli.service.instance.destroy_instance')
    def test_clean_up_creation_failed_destroy_all(self, mock):
        self.stderr = sys.stderr
        sys.stderr = StringIO.StringIO()
        failed =  maccli.facade.macfile.clean_up(MOCK_RESPONSE_INSTANCE_LIST_CREATION_FAILED_JSON, MACFILE_ON_FAILURE_DESTROY_ALL)
        mock.assert_any_call("id1")
        mock.assert_any_call("id2")
        self.assertTrue(failed)
        sys.stderr = self.stderr

    @mock.patch('maccli.service.instance.destroy_instance')
    def test_clean_up_configuration_error_destroy_all(self, mock):
        self.stderr = sys.stderr
        sys.stderr = StringIO.StringIO()
        failed =  maccli.facade.macfile.clean_up(MOCK_RESPONSE_INSTANCE_LIST_CONFIGURATION_ERROR_JSON, MACFILE_ON_FAILURE_DESTROY_ALL)
        mock.assert_any_call("id1")
        mock.assert_any_call("id2")
        self.assertTrue(failed)
        sys.stderr = self.stderr

    @mock.patch('maccli.service.instance.destroy_instance')
    def test_clean_up_creation_failed_destroy_others(self, mock):
        self.stderr = sys.stderr
        sys.stderr = StringIO.StringIO()
        failed =  maccli.facade.macfile.clean_up(MOCK_RESPONSE_INSTANCE_LIST_CREATION_FAILED_JSON, MACFILE_ON_FAILURE_DESTROY_OTHERS)
        mock.assert_any_call("id1")
        self.assertTrue(failed)
        sys.stderr = self.stderr

    @mock.patch('maccli.service.instance.destroy_instance')
    def test_clean_up_configuration_error_destroy_others(self, mock):
        self.stderr = sys.stderr
        sys.stderr = StringIO.StringIO()
        failed = maccli.facade.macfile.clean_up(MOCK_RESPONSE_INSTANCE_LIST_CONFIGURATION_ERROR_JSON, MACFILE_ON_FAILURE_DESTROY_OTHERS)
        mock.assert_any_call("id1")
        self.assertTrue(failed)
        sys.stderr = self.stderr

    @mock.patch('maccli.service.instance.facts')
    def test_two_public_ips_ok(self, mock_facts):
        INSTANCES=[{u'status': u'Ready', u'servername': u'mct-dbusa-n7k', u'lifespan': 42, u'ipv4': u'146.148.33.29', u'type': u'testing', u'id': u'n7km7na6hni5i3oug5023c0uq7', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'usa', u'environment_raw': [{u'PUBLIC_IP': u'master.PUBLIC_IP'}, {u'NODENAME': u'europe'}], u'version': 1.0, u'name': u'demo_database', u'macfile_role_name': u'master'}, u'system': {u'infrastructure': {u'hardware': u'https://www.googleapis.com/compute/v1/projects/manageacloud-instances/zones/REPLACE_ZONE/machineTypes/f1-micro', u'deployment': u'testing', u'location': u'us-central1-c', u'lifespan': 60, u'provider': u'manageacloud'}, u'role': {u'environment': {u'PUBLIC_IP': [u'146.148.33.29'], u'NODENAME': u'europe'}, u'cookbook_tag': u'demo_disperse_database', u'block_tags': [{}]}}}}, {u'status': u'Instance completed', u'servername': u'mct-dbeurope-bpe', u'lifespan': 42, u'ipv4': u'130.211.49.187', u'type': u'testing', u'id': u'bpe2u7hpjer8bkao5cr23r0cb2', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'europe', u'environment_raw': [{u'PUBLIC_IP': u'joining_master.PUBLIC_IP'}, {u'MASTER_IP': u'master.PUBLIC_IP'}, {u'NODENAME': u'usa'}], u'version': 1.0, u'name': u'demo_database', u'macfile_role_name': u'joining_master'}, u'system': {u'infrastructure': {u'hardware': u'https://www.googleapis.com/compute/v1/projects/manageacloud-instances/zones/REPLACE_ZONE/machineTypes/f1-micro', u'deployment': u'testing', u'location': u'europe-west1-c', u'lifespan': 60, u'provider': u'manageacloud'}, u'role': {u'environment': {u'PUBLIC_IP': u'joining_master.PUBLIC_IP', u'NODENAME': u'usa', u'MASTER_IP': u'master.PUBLIC_IP'}, u'cookbook_tag': u'demo_disperse_database', u'block_tags': [u'7k86iinhcues50ev75e1iev4pf']}}}}]
        VARS_RAW=[{u'PUBLIC_IP': u'joining_master.PUBLIC_IP'}, {u'MASTER_IP': u'master.PUBLIC_IP'}, {u'NODENAME': u'usa'}]
        var_clean, all_processed = maccli.facade.macfile.parse_instance_envs(VARS_RAW,INSTANCES)
        self.assertTrue(all_processed)


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

