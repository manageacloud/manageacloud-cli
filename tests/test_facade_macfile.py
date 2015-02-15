import unittest

import mock

from mock_data import *
import maccli.facade.macfile
from maccli.helper.exception import MacParseEnvException


class AuthTestCase(unittest.TestCase):
    @mock.patch('maccli.service.instance.credentials')
    def test_parse_envs(self, mock_credentials):
        mock_credentials.return_value = MOCK_CREDENTIALS
        clean_role = maccli.facade.macfile.parse_envs(MOCK_PARSE_ENVS_ROLE, MOCK_PARSE_ENVS_ROLE_CREATED)
        self.assertEqual(MOCK_PARSE_ENVS_ROLE_CLEAN, clean_role)

    @mock.patch('maccli.service.instance.credentials')
    def test_parse_envs(self, mock_credentials):
        mock_credentials.return_value = MOCK_CREDENTIALS
        self.assertRaises(MacParseEnvException, maccli.facade.macfile.parse_envs, MOCK_PARSE_ENVS_NO_ROLE, MOCK_PARSE_ENVS_NO_ROLE_CREATED)

    @mock.patch('maccli.service.instance.credentials')
    def test_parse_envs(self, mock_credentials):
        mock_credentials.return_value = MOCK_CREDENTIALS
        clean_role = maccli.facade.macfile.parse_envs(MOCK_PARSE_ENVS_ROLE, MOCK_PARSE_ENVS_ROLE_CREATED)
        self.assertEqual(MOCK_PARSE_ENVS_ROLE_CLEAN, clean_role)

    @mock.patch('maccli.service.instance.credentials')
    def test_parse_envs(self, mock_credentials):
        mock_credentials.return_value = MOCK_CREDENTIALS
        self.assertRaises(MacParseEnvException, maccli.facade.macfile.parse_envs, MOCK_PARSE_ENVS_NO_ROLE, MOCK_PARSE_ENVS_NO_ROLE_CREATED)

    @mock.patch('maccli.service.instance.facts')
    def test_parse_envs(self, mock_facts):
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        clean_role = maccli.facade.macfile.parse_envs(MOCK_PARSE_ENVS_ROLE_PRIV, MOCK_PARSE_ENVS_ROLE_CREATED)
        self.assertEqual(MOCK_PARSE_ENVS_ROLE_PRIV_CLEAN, clean_role)

    @mock.patch('maccli.service.instance.facts')
    def test_parse_envs(self, mock_facts):
        mock_facts.return_value = MOCK_FACTS_PRIV_NETWORK
        clean_role = maccli.facade.macfile.parse_envs(MOCK_PARSE_ENVS_ROLE_FACT, MOCK_PARSE_ENVS_ROLE_CREATED)
        self.assertEqual(MOCK_PARSE_ENVS_ROLE_FACT_CLEAN, clean_role)
