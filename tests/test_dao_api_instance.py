import unittest
import sys
import StringIO

import mock

import maccli.dao.api_instance
from mock_data import *


DEFAULT_DEPLOYMENT = "testing"
DEFAULT_PROVIDER = "manageacloud"
DEFAULT_BRANCH = "master"
DEFAULT_RELEASE = "any"
DEFAULT_CONFIGURATION = "cookbook_tag"
DEFAULT_LOCATION = "sfo1"
DEFAULT_SERVERNAME = "server_name"
DEFAULT_SERVER_ID = "serverid"
DEFAULT_HARDWARE = "512mb"
DEFAULT_LIFESPAN = 90
DEFAULT_ENVIRONMENT = ["KEY=VALUE"]
DEFAULT_HD = ["/dev/sda1:100"]
DEFAULT_PORT = [22]
DEFAULT_NET = ""
DEFAULT_METADATA = {'infrastructure': {
                       'version': '1.0infrastructure_version',
                       'name': 'infrastructure name',
                       'macfile_role_name': 'database',
                       'macfile_infrastructure_name': 'database_master',
                     }
                   }
DEFAULT_APPLYCHANGES = True

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.stderr = sys.stderr
        sys.stderr = self.buf = StringIO.StringIO()
        # pass

    def tearDown(self):
        sys.stderr = self.stderr
        # pass

    @mock.patch('maccli.helper.http.send_request')
    def test_instance_create(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_CREATE_JSON, MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW)
        json_response = maccli.dao.api_instance.create(DEFAULT_CONFIGURATION, DEFAULT_DEPLOYMENT, DEFAULT_LOCATION,
                                                       DEFAULT_SERVERNAME,
                                                       DEFAULT_PROVIDER, DEFAULT_RELEASE, DEFAULT_BRANCH,
                                                       DEFAULT_HARDWARE, DEFAULT_LIFESPAN, DEFAULT_ENVIRONMENT,
                                                       DEFAULT_HD, DEFAULT_PORT, DEFAULT_NET, DEFAULT_METADATA, DEFAULT_APPLYCHANGES)
        mock.assert_called_once_with("POST", "/instance", data=MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join("".split()), ' '.join(error.split()))
        self.assertEqual(json_response, MOCK_RESPONSE_INSTANCE_CREATE_JSON)


    @mock.patch('maccli.helper.http.send_request')
    def test_instance_create_error(self, mock):
        mock.return_value = (400, None, "Error Response")
        json_response = maccli.dao.api_instance.create(DEFAULT_CONFIGURATION, DEFAULT_DEPLOYMENT, DEFAULT_LOCATION,
                                                       DEFAULT_SERVERNAME,
                                                       DEFAULT_PROVIDER, DEFAULT_RELEASE, DEFAULT_BRANCH,
                                                       DEFAULT_HARDWARE, DEFAULT_LIFESPAN, DEFAULT_ENVIRONMENT,
                                                       DEFAULT_HD, DEFAULT_PORT, DEFAULT_NET, DEFAULT_METADATA, DEFAULT_APPLYCHANGES)
        mock.assert_called_once_with("POST", "/instance", data=MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_CREATE_ERROR.split()), ' '.join(error.split()))
        self.assertEqual(json_response, None)

    @mock.patch('maccli.helper.http.send_request')
    def test_instance_destroy_error(self, mock):
        mock.return_value = (400, None, "Error Response")
        json_response = maccli.dao.api_instance.destroy(DEFAULT_SERVER_ID)
        mock.assert_called_once_with("DELETE", "/instance/%s" % DEFAULT_SERVER_ID)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_DESTROY_ERROR.split()), ' '.join(error.split()))
        self.assertEqual(json_response, None)

    @mock.patch('maccli.helper.http.send_request')
    def test_instance_destroy_error_not_found(self, mock):
        mock.return_value = (404, None, "Error Response")
        json_response = maccli.dao.api_instance.destroy(DEFAULT_SERVERNAME)
        mock.assert_called_once_with("DELETE", "/instance/%s" % DEFAULT_SERVERNAME)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_DESTROY_NOT_FOUND.split()), ' '.join(error.split()))
        self.assertEqual(json_response, None)

    @mock.patch('maccli.helper.http.send_request')
    def test_instance_destroy_ok(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_DESTROY_JSON, MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW)
        json_response = maccli.dao.api_instance.destroy(DEFAULT_SERVERNAME)
        mock.assert_called_once_with("DELETE", "/instance/%s" % DEFAULT_SERVERNAME)
        self.assertEqual(json_response, MOCK_RESPONSE_INSTANCE_DESTROY_JSON)

    @mock.patch('maccli.helper.http.send_request')
    def test_instance_list(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_LIST_JSON, MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW)
        json_response = maccli.dao.api_instance.get_list()
        mock.assert_called_once_with("GET", "/instances")
        self.assertEqual(json_response, MOCK_RESPONSE_INSTANCE_LIST_JSON)
