import unittest
import sys
import StringIO

import mock

from mock_data import *
import maccli.command_cli


DEFAULT_DEPLOYMENT = "testing"
DEFAULT_PROVIDER = "manageacloud"
DEFAULT_LIFESPAN = 90
DEFAULT_BRANCH = "master"
DEFAULT_RELEASE = "any"
DEFAULT_PORT = [22]
DEFAULT_NET = ""


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()
        #pass

    def tearDown(self):
        sys.stdout = self.stdout
        #pass


    @mock.patch('maccli.service.instance.list_instances')
    def test_instance_list(self, mock_list_instances):
        mock_list_instances.return_value = MOCK_INSTANCE_LIST_JSON
        maccli.command_cli.instance_list()

    def test_instance_create_no_args(self):
        maccli.command_cli.instance_create(None, DEFAULT_DEPLOYMENT, None, None, DEFAULT_PROVIDER, DEFAULT_RELEASE,
                                           DEFAULT_BRANCH, None, DEFAULT_LIFESPAN, None, None, DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_NO_INPUT.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.provider.list_locations')
    def test_instance_create_cookbook(self, mock_list_locations):
        mock_list_locations.return_value = MOCK_LOCATION_LIST_JSON
        maccli.command_cli.instance_create("cookbook_tag", DEFAULT_DEPLOYMENT, None, None, DEFAULT_PROVIDER,
                                           DEFAULT_RELEASE, DEFAULT_BRANCH, None, DEFAULT_LIFESPAN, None, None,
                                           DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_ONLY_CONFIGURATION.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.provider.list_locations')
    def test_instance_create_cookbook_no_locations(self, mock_list_locations):
        mock_list_locations.return_value = MOCK_LOGIN_JSON_EMPTY
        maccli.command_cli.instance_create("cookbook_tag", DEFAULT_DEPLOYMENT, None, None, DEFAULT_PROVIDER,
                                           DEFAULT_RELEASE, DEFAULT_BRANCH, None, DEFAULT_LIFESPAN, None, None,
                                           DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_ONLY_CONFIGURATION_NO_LOCATIONS.split()),
                         ' '.join(out.split()))

    @mock.patch('maccli.service.provider.list_hardwares')
    def test_instance_create_production_cookbook_no_hardware(self, mock_list_hardwares):
        mock_list_hardwares.return_value = MOCK_HARDWARE_LIST_JSON
        maccli.command_cli.instance_create("cookbook_tag", "production", "sfo1", None, DEFAULT_PROVIDER,
                                           DEFAULT_RELEASE, DEFAULT_BRANCH, None, DEFAULT_LIFESPAN, None, None,
                                           DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_PRODUCTION_NO_HARDWARE.split()), ' '.join(out.split()))


    @mock.patch('maccli.service.instance.create_instance')
    def test_instance_create_development(self, mock_instance):
        mock_instance.return_value = MOCK_INSTANCE_CREATE_TESTING_OK_JSON
        maccli.command_cli.instance_create("cookbook_tag", DEFAULT_DEPLOYMENT, "sfo1", None, DEFAULT_PROVIDER,
                                           DEFAULT_RELEASE, DEFAULT_BRANCH, None, DEFAULT_LIFESPAN, None, None,
                                           DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_TESTING_OK.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.instance.create_instance')
    def test_instance_create_production(self, mock_instance):
        mock_instance.return_value = MOCK_INSTANCE_CREATE_PRODUCTION_OK_JSON
        maccli.command_cli.instance_create("cookbook_tag", "production", "sfo1", None, DEFAULT_PROVIDER,
                                           DEFAULT_RELEASE, DEFAULT_BRANCH, "512mb", DEFAULT_LIFESPAN, None, None,
                                           DEFAULT_PORT, DEFAULT_NET)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CREATE_INSTANCE_PRODUCTION_OK.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.configuration.search_configurations')
    def test_configuration_search(self, mock):
        mock.return_value = MOCK_CONFIGURATION_SEARCH_JSON
        maccli.command_cli.configuration_search(None, False)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CONFIGURATION_SEARCH.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.configuration.search_configurations')
    def test_configuration_search_keywords(self, mock):
        mock.return_value = MOCK_CONFIGURATION_SEARCH_JSON
        maccli.command_cli.configuration_search(None, True)
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CONFIGURATION_SEARCH_KEYWORDS.split()), ' '.join(out.split()))

    @mock.patch('maccli.service.configuration.list_configurations')
    def test_configuration_list(self, mock):
        mock.return_value = MOCK_CONFIGURATION_LIST_JSON
        maccli.command_cli.configuration_list()
        out = self.buf.getvalue()
        self.assertEqual(' '.join(OUTPUT_CONFIGURATION_LIST.split()), ' '.join(out.split()))


    @mock.patch('maccli.view.view_generic.general_help')
    def test_help(self, mock):
        maccli.command_cli.help()
        self.assertTrue(mock.called)

    @mock.patch('maccli.view.view_instance.show_instance_destroy_help')
    def test_instance_destroy_help(self, mock):
        maccli.command_cli.instance_destroy_help()
        self.assertTrue(mock.called)

    @mock.patch('maccli.view.view_instance.show_instance_ssh_help')
    def test_instance_ssh_help(self, mock):
        maccli.command_cli.instance_ssh_help()
        self.assertTrue(mock.called)

    @mock.patch('maccli.view.view_instance.show_instance_help')
    def test_instance_help(self, mock):
        maccli.command_cli.instance_help()
        self.assertTrue(mock.called)

    @mock.patch('maccli.view.view_cookbook.show_configurations_help')
    def test_instance_help(self, mock):
        maccli.command_cli.configuration_help()
        self.assertTrue(mock.called)

