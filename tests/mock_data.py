import json


class Mock_args(object):
    def __init__(self, cmd, subcmd):
        self.cmd = cmd
        self.subcmd = subcmd


class MockInstanceCreate_args(Mock_args):
    def __init__(self, cmd, subcmd):
        self.cmd = cmd
        self.subcmd = subcmd
        self.configuration = None
        self.deployment = None
        self.location = None
        self.name = None
        self.provider = None
        self.release = None
        self.branch = None
        self.hardware = None
        self.lifespan = None
        self.environment = None


class MockInstanceDestroy_args(Mock_args):
    def __init__(self, cmd, subcmd, name, id):
        self.cmd = cmd
        self.subcmd = subcmd
        self.name = name
        self.id = id


class MockConfiguration_Args(Mock_args):
    def __init__(self, cmd, subcmd, keyword, url):
        self.cmd = cmd
        self.subcmd = subcmd
        self.keyword = keyword
        self.url = url


class MockInstanceSSH_args(MockInstanceDestroy_args):
    pass


MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW = '{"hardware": "512mb", "cookbook_tag": "cookbook_tag", "location": "sfo1", "branch": "master", "deployment": "testing", "release": "any", "environments": ["KEY=VALUE"], "servername": "server_name", "provider": "manageacloud", "lifespan": 90}'

MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW = '{"servername":"","id":"c01br5mu83hs0v3jogsetm0acj","type":"testing","status":"Creating instance"}'
MOCK_RESPONSE_INSTANCE_CREATE_JSON = json.loads(MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW)
MOCK_RESPONSE_INSTANCE_CREATE_ERROR = 'Error while building request: Error Response'

MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW = '{"servername":"servername","id":"s017frnl7ah6lqljkc4omt8h4k","type":"testing","status":"Queued to be destroyed"}'
MOCK_RESPONSE_INSTANCE_DESTROY_JSON = json.loads(MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW)
MOCK_RESPONSE_INSTANCE_DESTROY_ERROR = 'Error with parameters: Error Response'
MOCK_RESPONSE_INSTANCE_DESTROY_NOT_FOUND = 'Server server_name not found'

MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW = '[{"servername":"mct-f2c","id":"vpeuf8gdv76v8feu40icklm9h2","type":"testing","status":"Ready"}]'
MOCK_RESPONSE_INSTANCE_LIST_JSON = json.loads(MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW)

MOCK_USER = 'fake_mac_user'
MOCK_PASSWORD = 'fake_mac_password'
MOCK_APIKEY = '5e8520c1a6a0fb6d9cea28d06b82a0573c1144ab26efcc4a66ec16b1aec9bcab'

MOCK_LOGIN_JSON_RAW = '{"username":"fake_mac_user","apiKey":"5e8520c1a6a0fb6d9cea28d06b82a0573c1144ab26efcc4a66ec16b1aec9bcab"}'
MOCK_LOGIN_JSON = json.loads(MOCK_LOGIN_JSON_RAW)

MOCK_INSTANCE_LIST_JSON_RAW = '[{"servername":"mct-277","id": "serverid","status":"Ready","type":"development"}]'
MOCK_INSTANCE_LIST_JSON = json.loads(MOCK_INSTANCE_LIST_JSON_RAW)

MOCK_LOCATION_LIST_JSON_RAW = '[{"id":"ams3","description":"9/Amsterdam 3","release":"debian"},{"id":"lon1","description":"7/London 1","release":"debian"},{"id":"nyc3","description":"8/New York 3","release":"debian"},{"id":"sfo1","description":"3/San Francisco 1","release":"debian"},{"id":"sgp1","description":"6/Singapore 1","release":"debian"},{"id":"nyc2","description":"4/New York 2","release":"debian"},{"id":"ams2","description":"5/Amsterdam 2","release":"debian"}]'
MOCK_LOCATION_LIST_JSON = json.loads(MOCK_LOCATION_LIST_JSON_RAW)

MOCK_HARDWARE_LIST_JSON_RAW = '[{"id":"512mb","processors":[{"cores":1.0,"speed":1.0}],"ram":512,"volumes":[{"type":"LOCAL","size":20.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"1gb","processors":[{"cores":1.0,"speed":1.0}],"ram":1024,"volumes":[{"type":"LOCAL","size":30.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"2gb","processors":[{"cores":2.0,"speed":2.0}],"ram":2048,"volumes":[{"type":"LOCAL","size":40.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"4gb","processors":[{"cores":2.0,"speed":2.0}],"ram":4096,"volumes":[{"type":"LOCAL","size":60.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"8gb","processors":[{"cores":4.0,"speed":4.0}],"ram":8192,"volumes":[{"type":"LOCAL","size":80.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"16gb","processors":[{"cores":8.0,"speed":8.0}],"ram":16384,"volumes":[{"type":"LOCAL","size":160.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"32gb","processors":[{"cores":12.0,"speed":12.0}],"ram":32768,"volumes":[{"type":"LOCAL","size":320.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"48gb","processors":[{"cores":16.0,"speed":16.0}],"ram":49152,"volumes":[{"type":"LOCAL","size":480.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"64gb","processors":[{"cores":20.0,"speed":20.0}],"ram":65536,"volumes":[{"type":"LOCAL","size":640.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}}]'
MOCK_HARDWARE_LIST_JSON = json.loads(MOCK_HARDWARE_LIST_JSON_RAW)

MOCK_INSTANCE_CREATE_TESTING_OK_JSON_RAW = '{"servername":"","id":"qse0hca2jj1di63k8bidvmffig","type":"testing","status":"Creating instance"}'
MOCK_INSTANCE_CREATE_TESTING_OK_JSON = json.loads(MOCK_INSTANCE_CREATE_TESTING_OK_JSON_RAW)

MOCK_INSTANCE_CREATE_PRODUCTION_OK_JSON_RAW = '{"servername":"","id":"s017frnl7ah6lqljkc4omt8h4k","type":"production","status":"Creating instance"}'
MOCK_INSTANCE_CREATE_PRODUCTION_OK_JSON = json.loads(MOCK_INSTANCE_CREATE_PRODUCTION_OK_JSON_RAW)

MOCK_INSTANCE_CREDENTIALS_PRIVKEY_JSON_RAW = '{"ip":"104.236.164.139","port":22,"user":"root","password":"","privateKey":"privkey"}'
MOCK_INSTANCE_CREDENTIALS_PRIVKEY_JSON = json.loads(MOCK_INSTANCE_CREDENTIALS_PRIVKEY_JSON_RAW)

MOCK_INSTANCE_CREDENTIALS_PASS_JSON_RAW = '{"ip":"104.236.164.139","port":22,"user":"root","password":"pass","privateKey":""}'
MOCK_INSTANCE_CREDENTIALS_PASS_JSON = json.loads(MOCK_INSTANCE_CREDENTIALS_PASS_JSON_RAW)

MOCK_CONFIGURATION_SEARCH_JSON_RAW = '[{"tag":"vaadinrest_web_client","name":"VaadinREST web client.","summary":"A simple deployment for a vaadin rest client","url":"https://manageacloud.com/configuration/vaadinrest_web_client"},{"tag":"tutanota_email_client_debian_wheezy_70","name":"Tutanota email client","summary":"Installs tutanota email client with Nginx and a self-signed certificate","url":"https://manageacloud.com/configuration/tutanota_email_client_debian_wheezy_70"},{"tag":"bolt_cms_amazon_2014032","name":"Bolt CMS","summary":"Basic bolt cms / blog installation ","url":"https://manageacloud.com/configuration/bolt_cms_amazon_2014032"},{"tag":"django_helpdesk_amazon_2014032","name":"Django Helpdesk","summary":"A Django powered ticket tracker for small enterprise","url":"https://manageacloud.com/configuration/django_helpdesk_amazon_2014032"},{"tag":"nagios_408_template","name":"Nagios 4.0.8 template","summary":"nagios 4, nagios plugins and nrpe","url":"https://manageacloud.com/configuration/nagios_408_template"},{"tag":"guacad_tomcat7","name":"guacamole server and aplication with tomcat7","summary":"guacamole server and application and tomcat7","url":"https://manageacloud.com/configuration/guacad_tomcat7"},{"tag":"redis-server-template","name":"redis-server-template","summary":"Download Redis tarball, extract, compile, configure","url":"https://manageacloud.com/configuration/redis-server-template"},{"tag":"tutanota_email_client_amazon_2014032","name":"Tutanota email client","summary":"Installs tutanota email client with Nginx and a self-signed certificate","url":"https://manageacloud.com/configuration/tutanota_email_client_amazon_2014032"},{"tag":"anchor_cms_ubuntu_trusty_tahr_1404","name":"Anchor CMS","summary":"Anchor CMS and Blog System","url":"https://manageacloud.com/configuration/anchor_cms_ubuntu_trusty_tahr_1404"}]'
MOCK_CONFIGURATION_SEARCH_JSON = json.loads(MOCK_CONFIGURATION_SEARCH_JSON_RAW)

MOCK_CONFIGURATION_LIST_JSON_RAW = '[{"tag":"wordpress_128","name":"Wordpress","summary":"","url":"https://manageacloud.com/configuration/wordpress_128"},{"tag":"test_server","name":"Test server","summary":"","url":"https://manageacloud.com/configuration/test_server"}]'
MOCK_CONFIGURATION_LIST_JSON = json.loads(MOCK_CONFIGURATION_LIST_JSON_RAW)

MOCK_LOGIN_JSON_EMPTY = json.loads("[]")

OUTPUT_HARDWARES_NO_CREDENTIALS = '''There is no credentials available in your account for the provider manageacloud

Please login in your account in https://manageacloud.com and deploy a production server using the supplier manageacloud

You just need to make this action once.
'''

OUTPUT_CONFIGURATION_LIST = '''
+---------------+-------------+---------+
| Tag           | Title       | Summary |
+---------------+-------------+---------+
| wordpress_128 | Wordpress   |         |
| test_server   | Test server |         |
+---------------+-------------+---------+

Search more at https://manageacloud.com/cookbooks

'''

OUTPUT_CONFIGURATION_SEARCH = '''+----------------------------------------+----------------------------------------------+-------------------------------------------------------------------------+
| Tag                                    | Title                                        | Summary                                                                 |
+----------------------------------------+----------------------------------------------+-------------------------------------------------------------------------+
| vaadinrest_web_client                  | VaadinREST web client.                       | A simple deployment for a vaadin rest client                            |
| tutanota_email_client_debian_wheezy_70 | Tutanota email client                        | Installs tutanota email client with Nginx and a self-signed certificate |
| bolt_cms_amazon_2014032                | Bolt CMS                                     | Basic bolt cms / blog installation                                      |
| django_helpdesk_amazon_2014032         | Django Helpdesk                              | A Django powered ticket tracker for small enterprise                    |
| nagios_408_template                    | Nagios 4.0.8 template                        | nagios 4, nagios plugins and nrpe                                       |
| guacad_tomcat7                         | guacamole server and aplication with tomcat7 | guacamole server and application and tomcat7                            |
| redis-server-template                  | redis-server-template                        | Download Redis tarball, extract, compile, configure                     |
| tutanota_email_client_amazon_2014032   | Tutanota email client                        | Installs tutanota email client with Nginx and a self-signed certificate |
| anchor_cms_ubuntu_trusty_tahr_1404     | Anchor CMS                                   | Anchor CMS and Blog System                                              |
+----------------------------------------+----------------------------------------------+-------------------------------------------------------------------------+

Search more at https://manageacloud.com/cookbooks

'''

OUTPUT_CONFIGURATION_SEARCH_KEYWORDS = '''+----------------------------------------+-------------------------------------------------------------------------------+
| Tag                                    | Url                                                                           |
+----------------------------------------+-------------------------------------------------------------------------------+
| vaadinrest_web_client                  | https://manageacloud.com/configuration/vaadinrest_web_client                  |
| tutanota_email_client_debian_wheezy_70 | https://manageacloud.com/configuration/tutanota_email_client_debian_wheezy_70 |
| bolt_cms_amazon_2014032                | https://manageacloud.com/configuration/bolt_cms_amazon_2014032                |
| django_helpdesk_amazon_2014032         | https://manageacloud.com/configuration/django_helpdesk_amazon_2014032         |
| nagios_408_template                    | https://manageacloud.com/configuration/nagios_408_template                    |
| guacad_tomcat7                         | https://manageacloud.com/configuration/guacad_tomcat7                         |
| redis-server-template                  | https://manageacloud.com/configuration/redis-server-template                  |
| tutanota_email_client_amazon_2014032   | https://manageacloud.com/configuration/tutanota_email_client_amazon_2014032   |
| anchor_cms_ubuntu_trusty_tahr_1404     | https://manageacloud.com/configuration/anchor_cms_ubuntu_trusty_tahr_1404     |
+----------------------------------------+-------------------------------------------------------------------------------+

Search more at https://manageacloud.com/cookbooks

'''

OUTPUT_CREATE_INSTANCE_PRODUCTION_OK = '''+---------------+----------------------------+------------+-------------------+
| Instance name |        Instance ID         |    Type    |       Status      |
+---------------+----------------------------+------------+-------------------+
|               | s017frnl7ah6lqljkc4omt8h4k | production | Creating instance |
+---------------+----------------------------+------------+-------------------+'''

OUTPUT_CREATE_INSTANCE_TESTING_OK = '''+---------------+----------------------------+---------+-------------------+
| Instance name |        Instance ID         |   Type  |       Status      |
+---------------+----------------------------+---------+-------------------+
|               | qse0hca2jj1di63k8bidvmffig | testing | Creating instance |
+---------------+----------------------------+---------+-------------------+
'''

OUTPUT_CREATE_INSTANCE_NO_INPUT = '''--configuration parameter is required.

You can list your configurations:

    mac configuration list

or search public configurations

    mac configuration search

To create a new instance with this configuration:

    mac instance create -c <configuration tag>

Show more help:

    mac instance -h

'''

OUTPUT_CREATE_INSTANCE_ONLY_CONFIGURATION_NO_LOCATIONS = '''--location parameter not set. You must choose the location.

Available locations:

There is not locations available for configuration cookbook_tag and provider manageacloud

Show more help:

    mac instance -h

'''

OUTPUT_CREATE_INSTANCE_ONLY_CONFIGURATION = '''--location parameter not set. You must choose the location.

Available locations:

+--------------+----------+-------------------+
| Distribution | Location | Description       |
+--------------+----------+-------------------+
|    debian    |   ams3   | 9/Amsterdam 3     |
|    debian    |   lon1   | 7/London 1        |
|    debian    |   nyc3   | 8/New York 3      |
|    debian    |   sfo1   | 3/San Francisco 1 |
|    debian    |   sgp1   | 6/Singapore 1     |
|    debian    |   nyc2   | 4/New York 2      |
|    debian    |   ams2   | 5/Amsterdam 2     |
+--------------+----------+-------------------+

Example:

    mac instance create -c cookbook_tag -l ams3


Show more help:

    mac instance -h

'''

OUTPUT_CREATE_INSTANCE_PRODUCTION_NO_HARDWARE = '''
--hardware not found. You must choose the hardware.

Available hardware:

+-------+-------+-------+---------+
|    Id |   RAM | Cores |      HD |
+-------+-------+-------+---------+
| 512mb |   512 |   1.0 |  20.0Gb |
|   1gb |  1024 |   1.0 |  30.0Gb |
|   2gb |  2048 |   2.0 |  40.0Gb |
|   4gb |  4096 |   2.0 |  60.0Gb |
|   8gb |  8192 |   4.0 |  80.0Gb |
|  16gb | 16384 |   8.0 | 160.0Gb |
|  32gb | 32768 |  12.0 | 320.0Gb |
|  48gb | 49152 |  16.0 | 480.0Gb |
|  64gb | 65536 |  20.0 | 640.0Gb |
+-------+-------+-------+---------+

Example:

    mac instance create  -c cookbook_tag -d production -l sfo1 -hw 512mb

'''