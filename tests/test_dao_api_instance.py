import unittest, sys, StringIO
import mock
import dao.api_instance
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


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.stderr = sys.stderr
        sys.stderr = self.buf = StringIO.StringIO()
        #pass

    def tearDown(self):
        sys.stderr = self.stderr
        #pass

    @mock.patch('helper.http.send_request')
    def test_instance_create(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_CREATE_JSON, MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW)
        json = dao.api_instance.create(DEFAULT_CONFIGURATION, DEFAULT_DEPLOYMENT, DEFAULT_LOCATION, DEFAULT_SERVERNAME,
                                DEFAULT_PROVIDER, DEFAULT_RELEASE, DEFAULT_BRANCH, DEFAULT_HARDWARE)
        mock.assert_called_once_with("POST", "/instance", data=MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join("".split()), ' '.join(error.split()))
        self.assertEqual(json, MOCK_RESPONSE_INSTANCE_CREATE_JSON)


    @mock.patch('helper.http.send_request')
    def test_instance_create_error(self, mock):
        mock.return_value = (400, None, "Error Response")
        json = dao.api_instance.create(DEFAULT_CONFIGURATION, DEFAULT_DEPLOYMENT, DEFAULT_LOCATION, DEFAULT_SERVERNAME,
                                DEFAULT_PROVIDER, DEFAULT_RELEASE, DEFAULT_BRANCH, DEFAULT_HARDWARE)
        mock.assert_called_once_with("POST", "/instance", data=MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_CREATE_ERROR.split()), ' '.join(error.split()))
        self.assertEqual(json, None)

    @mock.patch('helper.http.send_request')
    def test_instance_destroy_error(self, mock):
        mock.return_value = (400, None, "Error Response")
        json = dao.api_instance.destroy(DEFAULT_SERVERNAME, DEFAULT_SERVER_ID)
        mock.assert_called_once_with("DELETE", "/instance", data=MOCK_INSTANCE_DESTROY_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_DESTROY_ERROR.split()), ' '.join(error.split()))
        self.assertEqual(json, None)

    @mock.patch('helper.http.send_request')
    def test_instance_destroy_error_not_found(self, mock):
        mock.return_value = (404, None, "Error Response")
        json = dao.api_instance.destroy(DEFAULT_SERVERNAME, DEFAULT_SERVER_ID)
        mock.assert_called_once_with("DELETE", "/instance", data=MOCK_INSTANCE_DESTROY_PARAMETERS_JSON_RAW)
        error = self.buf.getvalue()
        self.assertEqual(' '.join(MOCK_RESPONSE_INSTANCE_DESTROY_NOT_FOUND.split()), ' '.join(error.split()))
        self.assertEqual(json, None)

    @mock.patch('helper.http.send_request')
    def test_instance_destroy_ok(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_DESTROY_JSON, MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW)
        json = dao.api_instance.destroy(DEFAULT_SERVERNAME, DEFAULT_SERVER_ID)
        mock.assert_called_once_with("DELETE", "/instance", data=MOCK_INSTANCE_DESTROY_PARAMETERS_JSON_RAW)
        self.assertEqual(json, MOCK_RESPONSE_INSTANCE_DESTROY_JSON)

    @mock.patch('helper.http.send_request')
    def test_instance_list(self, mock):
        mock.return_value = (200, MOCK_RESPONSE_INSTANCE_LIST_JSON, MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW)
        json = dao.api_instance.get_list()
        mock.assert_called_once_with("GET", "/instances")
        self.assertEqual(json, MOCK_RESPONSE_INSTANCE_LIST_JSON)
