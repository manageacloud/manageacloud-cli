import json
import maccli
from collections import OrderedDict

class Mock_yaml_args(object):
    def __init__(self):
        self.branch='master'
        self.cmd='instance'
        self.configuration='database'
        self.debug=True
        self.deployment='testing'
        self.environment=None
        self.hardware=None
        self.hd=None
        self.lifespan=None
        self.location='us-central1-c'
        self.name=None
        self.port=None
        self.provider='manageacloud'
        self.release='any'
        self.subcmd='create'
        self.verbose=False
        self.yaml=True

MOCK_MACFILE = """mac: %s
description: Manageacloud CLI
name: manageacloud.com
version: '1.0'
roles:
  default:
    instance create:
      branch: master
      configuration: database
infrastructures:
  default:
    deployment: testing
    location: us-central1-c
    name: ''
    provider: manageacloud
    release: any
    role: default
    amount: 1
""" % maccli.__version__

MACFILE_PARAMS_INVALID = ['NOTEXIST=0', 'PARAM2=VALUE2']
MACFILE_PARAMS_VALID = ['VERSION=1.0', 'LOCATION=us-central1-c', 'AMOUNT=1']
MACFILE_PARAMS_EMPTY = []
MACFILE_PARAMS_ONE_MISSING = ['VERSION=1.0', 'LOCATION=us-central1-c']

MOCK_MACFILE_PARAMS = """mac: 0.5a1
description: Manageacloud CLI
name: manageacloud.com
version: {VERSION}
roles:
  default:
    instance create:
      branch: master
      configuration: database
infrastructures:
  default:
    deployment: testing
    location: {LOCATION}
    name: ''
    provider: manageacloud
    release: any
    role: default
    amount: {AMOUNT}
"""


MOCK_MACFILE_PARAMS_2 = """mac: 0.9.6
description: test
name: test
version: test

resources:

  build_lb:
    create bash:
      aws elb create-load-balancer
        --load-balancer-name lb-connection-draining
        --listeners Protocol=HTTPS,LoadBalancerPort=443,InstanceProtocol=HTTP,InstancePort=80,SSLCertificateId=arn:aws:iam::my:server-certificate/Manageacloud
        --security-groups sg-id
        --region infrastructure.inf_app.location
        --subnets subnet-id
    destroy bash:
      aws elb delete-load-balancer
      --load-balancer-name lb-connection-draining
      --region us-east-1

  health_check:
    create bash:
      aws elb configure-health-check
        --load-balancer-name lb-connection-draining
        --health-check Target=HTTP:80/diagnostic,Interval=15,UnhealthyThreshold=2,HealthyThreshold=2,Timeout=5
        --region us-east-1

  connetion_draining:
    create bash:
      aws elb modify-load-balancer-attributes --load-balancer-name lb-connection-draining
      --load-balancer-attributes "{\"ConnectionDraining\":{\"Enabled\":true,\"Timeout\":300}}"

infrastructures:

  build_lb_inf:
    resource: build_lb

  health_check_inf:
    resource: health_check

  connetion_draining_inf:
    resource: connetion_draining
"""

MOCK_MACFILE_PARAMS_VALID = """mac: 0.5a1
description: Manageacloud CLI
name: manageacloud.com
version: 1.0
roles:
  default:
    instance create:
      branch: master
      configuration: database
infrastructures:
  default:
    deployment: testing
    location: us-central1-c
    name: ''
    provider: manageacloud
    release: any
    role: default
    amount: 1
"""

class Mock_args(object):
    def __init__(self, cmd, subcmd):
        self.debug = False
        self.quiet = False
        self.verbose = False
        self.cmd = cmd
        self.subcmd = subcmd


class MockInstanceCreate_args(Mock_args):
    def __init__(self, cmd, subcmd):
        self.debug = False
        self.quiet = False
        self.verbose = False
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
        self.hd = None
        self.port = None
        self.net = None
        self.yaml = None


class MockInstanceDestroy_args(Mock_args):
    def __init__(self, cmd, subcmd, name, id):
        self.debug = False
        self.quiet = False
        self.verbose = False
        self.cmd = cmd
        self.subcmd = subcmd
        self.name = name
        self.id = id


class MockConfiguration_Args(Mock_args):
    def __init__(self, cmd, subcmd, keyword, url):
        self.debug = False
        self.quiet = False
        self.verbose = False
        self.cmd = cmd
        self.subcmd = subcmd
        self.keyword = keyword
        self.url = url


class MockInstanceSSH_args(MockInstanceDestroy_args):
    def __init__(self, cmd, subcmd, instance_id, command):
        self.debug = False
        self.quiet = False
        self.verbose = False
        self.cmd = cmd
        self.subcmd = subcmd
        self.id = instance_id
        self.command = command


MOCK_INSTANCE_CREATE_PARAMETERS_JSON_RAW = '{"servername": "server_name", "environments": ["KEY=VALUE"], "hardware": "512mb", "cookbook_tag": "cookbook_tag", "deployment": "testing", "port": [22], "hd": ["/dev/sda1:100"], "lifespan": 90, "apply_changes": true, "location": "sfo1", "branch": "master", "provider": "manageacloud", "release": "any", "net": "", "metadata": "{\\"infrastructure\\": {\\"macfile_infrastructure_name\\": \\"database_master\\", \\"macfile_role_name\\": \\"database\\", \\"version\\": \\"1.0infrastructure_version\\", \\"name\\": \\"infrastructure name\\"}}"}'

MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW = '{"servername":"","id":"c01br5mu83hs0v3jogsetm0acj","type":"testing","status":"Creating instance"}'
MOCK_RESPONSE_INSTANCE_CREATE_JSON = json.loads(MOCK_RESPONSE_INSTANCE_CREATE_JSON_RAW)
MOCK_RESPONSE_INSTANCE_CREATE_ERROR = 'Error while building request: Error Response'

MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW = '{"servername":"servername","id":"s017frnl7ah6lqljkc4omt8h4k","type":"testing","status":"Queued to be destroyed"}'
MOCK_RESPONSE_INSTANCE_DESTROY_JSON = json.loads(MOCK_RESPONSE_INSTANCE_DESTROY_JSON_RAW)
MOCK_RESPONSE_INSTANCE_DESTROY_ERROR = 'Error with parameters: Error Response'
MOCK_RESPONSE_INSTANCE_DESTROY_NOT_FOUND = 'Server server_name not found'

MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW = '[{"servername":"mct-f2c","id":"vpeuf8gdv76v8feu40icklm9h2","type":"testing","status":"Ready"}]'
MOCK_RESPONSE_INSTANCE_LIST_JSON = json.loads(MOCK_RESPONSE_INSTANCE_LIST_JSON_RAW)

MOCK_RESPONSE_INSTANCE_LIST_CREATION_FAILED_JSON_RAW = '[{"servername":"name1","id":"id1","type":"testing","status":"Ready"}, {"servername":"name2","id":"id2","type":"testing","status":"Creation failed"}]'
MOCK_RESPONSE_INSTANCE_LIST_CREATION_FAILED_JSON = json.loads(MOCK_RESPONSE_INSTANCE_LIST_CREATION_FAILED_JSON_RAW)

MOCK_RESPONSE_INSTANCE_LIST_CONFIGURATION_ERROR_JSON_RAW = '[{"servername":"name1","id":"id1","type":"testing","status":"Ready"}, {"servername":"name2","id":"id2","type":"testing","status":"Configuration Error"}]'
MOCK_RESPONSE_INSTANCE_LIST_CONFIGURATION_ERROR_JSON = json.loads(MOCK_RESPONSE_INSTANCE_LIST_CONFIGURATION_ERROR_JSON_RAW)



MOCK_USER = 'fake_mac_user'
MOCK_PASSWORD = 'fake_mac_password'
MOCK_APIKEY = '5e8520c1a6a0fb6d9cea28d06b82a0573c1144ab26efcc4a66ec16b1aec9bcab'

MOCK_LOGIN_JSON_RAW = '{"username":"fake_mac_user","apiKey":"5e8520c1a6a0fb6d9cea28d06b82a0573c1144ab26efcc4a66ec16b1aec9bcab"}'
MOCK_LOGIN_JSON = json.loads(MOCK_LOGIN_JSON_RAW)

MOCK_INSTANCE_LIST_JSON_RAW = '[{"servername":"mct-277","ipv4":"1.2.3.4","id": "serverid","status":"Ready","type":"development"}]'
MOCK_INSTANCE_LIST_JSON = json.loads(MOCK_INSTANCE_LIST_JSON_RAW)

MOCK_INSTANCE_LARGE_LIST_JSON_RAW = '[{"status": "Ready", "servername": "mcp-prod-b55", "lifespan": 0, "ipv4": "166.78.136.158", "type": "production", "id": "vcb553nb5p40km5tc1ofl1t0t8", "metadata": {"system": {"infrastructure": {"hardware": "DFW/2", "deployment": "production", "location": "DFW", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.113", "IP_RANGE": "10.0.1.114-126"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-7a6", "lifespan": 0, "ipv4": "166.78.137.49", "type": "production", "id": "oli3vhvbko0g4054ht89dcamdd", "metadata": {"system": {"infrastructure": {"hardware": "DFW/2", "deployment": "production", "location": "DFW", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.129", "IP_RANGE": "10.0.1.130-142"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-d8b", "lifespan": 0, "ipv4": "162.209.99.168", "type": "production", "id": "2sh6jr9eb3gqgls3gasi7nb9q2", "metadata": {"system": {"infrastructure": {"hardware": "IAD/2", "deployment": "production", "location": "IAD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.145", "IP_RANGE": "10.0.1.146-158"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-116", "lifespan": 0, "ipv4": "119.9.12.64", "type": "production", "id": "8sv3g3hv5boodmdrerd138a97t", "metadata": {"system": {"infrastructure": {"hardware": "SYD/2", "deployment": "production", "location": "SYD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.161", "IP_RANGE": "10.0.1.162-174"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-e83", "lifespan": 0, "ipv4": "119.9.77.238", "type": "production", "id": "t9i654isc8eki8o10rvuo73sdh", "metadata": {"system": {"infrastructure": {"hardware": "HKG/2", "deployment": "production", "location": "HKG", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"VPN_SERVER": "10.0.0.241", "IP_RANGE": "10.0.0.242-254"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-c27", "lifespan": 0, "ipv4": "119.9.12.85", "type": "production", "id": "quhae43uf9rhikrc04i7773jub", "metadata": {"system": {"infrastructure": {"hardware": "SYD/2", "deployment": "production", "location": "SYD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"VPN_SERVER": "10.0.1.1", "IP_RANGE": "10.0.1.2-14"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-338", "lifespan": 0, "ipv4": "104.239.233.93", "type": "production", "id": "ks5se21c94qtknld46f2ojtls2", "metadata": {"system": {"infrastructure": {"hardware": "IAD/2", "deployment": "production", "location": "IAD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"VPN_SERVER": "10.0.1.17", "IP_RANGE": "10.0.1.18-30"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-e44", "lifespan": 0, "ipv4": "192.237.171.170", "type": "production", "id": "bbrq4nrak045ctcoi00r98op6t", "metadata": {"system": {"infrastructure": {"hardware": "ORD/2", "deployment": "production", "location": "ORD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"VPN_SERVER": "10.0.1.33", "IP_RANGE": "10.0.1.34-46"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-311", "lifespan": 0, "ipv4": "50.56.176.219", "type": "production", "id": "n9db3hcqaf89jgp6up3ih2kafu", "metadata": {"system": {"infrastructure": {"hardware": "DFW/2", "deployment": "production", "location": "DFW", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"VPN_SERVER": "10.0.1.49", "IP_RANGE": "10.0.1.50-62"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-bb1", "lifespan": 0, "ipv4": "192.237.171.181", "type": "production", "id": "pv4g825epato1knia4jmgrtg89", "metadata": {"system": {"infrastructure": {"hardware": "ORD/2", "deployment": "production", "location": "ORD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.81", "IP_RANGE": "10.0.1.82-94"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-557", "lifespan": 0, "ipv4": "192.237.171.232", "type": "production", "id": "s1dcsq23upo960a1i8duc9ed1l", "metadata": {"system": {"infrastructure": {"hardware": "ORD/2", "deployment": "production", "location": "ORD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.97", "IP_RANGE": "10.0.1.98-110"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-be8", "lifespan": 0, "ipv4": "119.9.74.218", "type": "production", "id": "fh130rdtcbqfgthuairqujoui9", "metadata": {"system": {"infrastructure": {"hardware": "HKG/2", "deployment": "production", "location": "HKG", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.177", "IP_RANGE": "10.0.1.178-190"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}, {"status": "Ready", "servername": "mcp-prod-b46", "lifespan": 0, "ipv4": "104.130.231.103", "type": "production", "id": "ok79bgskddall137h50elph4e6", "metadata": {"system": {"infrastructure": {"hardware": "IAD/2", "deployment": "production", "location": "IAD", "lifespan": -1, "provider": "rackspaceus"}, "role": {"environment": {"PASSWORD": "4br4c4d4br4yeh", "VPN_SERVER": "10.0.1.193", "IP_RANGE": "10.0.1.194-206"}, "cookbook_tag": "base_worker", "block_tags": ["meeou161t7i4uhtuj6i0utc7n"]}}}}]'
MOCK_INSTANCE_LARGE_LIST_JSON = json.loads(MOCK_INSTANCE_LARGE_LIST_JSON_RAW)


MOCK_INSTANCE_LIST_INFRASTRUCTURE_RAW = [{u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u't78mro0idv1thf0p2vodbbgbe2', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'tl5git179967na458d2vkmm19t', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}, {u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'dl9lii485iuhu77ggtaaeph9nr', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'gignmnqg30g5kjaooa6ut6s48o', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}, {u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 89, u'ipv4': u'', u'type': u'testing', u'id': u'adh5dasi7s78vva68od24mtguj', u'metadata': {u'infrastructure': {u'role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing', u'infrastructure_name': u'shared_memcache'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 89, u'ipv4': u'', u'type': u'testing', u'id': u't72nkmvlf7ivsju5ggdn85embt', u'metadata': {u'infrastructure': {u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'role_name': u'engine', u'version': u'2.0', u'name': u'testing', u'infrastructure_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}]
MOCK_INSTANCE_LIST_INFRASTRUCTURE_CLEAN = [{u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u't78mro0idv1thf0p2vodbbgbe2', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'tl5git179967na458d2vkmm19t', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}, {u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'dl9lii485iuhu77ggtaaeph9nr', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'shared_memcache', u'macfile_role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}, {u'status': u'Creating instance', u'servername': u'engine', u'lifespan': 78, u'ipv4': u'', u'type': u'testing', u'id': u'gignmnqg30g5kjaooa6ut6s48o', u'metadata': {u'infrastructure': {u'macfile_infrastructure_name': u'engine', u'environment_raw': [{u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}], u'version': u'1.0', u'name': u'testing', u'macfile_role_name': u'engine'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {u'environment': {u'SHARED_MEMCACHE_IP': u'shared_memcache.PRIVATE_IP'}}}}}, {u'status': u'Creating instance', u'servername': u'memcache', u'lifespan': 89, u'ipv4': u'', u'type': u'testing', u'id': u'adh5dasi7s78vva68od24mtguj', u'metadata': {u'infrastructure': {u'role_name': u'shared_memcache', u'version': u'1.0', u'name': u'testing', u'infrastructure_name': u'shared_memcache'}, u'system': {u'infrastructure': {u'hardware': u'512mb', u'deployment': u'testing', u'location': u'sfo1', u'lifespan': 90, u'provider': u'manageacloud'}, u'role': {}}}}]

MOCK_LOCATION_LIST_JSON_RAW = '[{"id":"ams3","description":"9/Amsterdam 3","release":"debian"},{"id":"lon1","description":"7/London 1","release":"debian"},{"id":"nyc3","description":"8/New York 3","release":"debian"},{"id":"sfo1","description":"3/San Francisco 1","release":"debian"},{"id":"sgp1","description":"6/Singapore 1","release":"debian"},{"id":"nyc2","description":"4/New York 2","release":"debian"},{"id":"ams2","description":"5/Amsterdam 2","release":"debian"}]'
MOCK_LOCATION_LIST_JSON = json.loads(MOCK_LOCATION_LIST_JSON_RAW)

MOCK_LOCATION_LIST_RELEASES_JSON_RAW = '[{"release": "amazon", "id": "lon1", "description": "7/London 1"}, {"release": "centos", "id": "ams3", "description": "9/Amsterdam 3"}, {"release": "centos", "id": "sgp1", "description": "6/Singapore 1"}, {"release": "amazon", "id": "sfo1", "description": "3/San Francisco 1"}, {"release": "centos", "id": "ams2", "description": "5/Amsterdam 2"}, {"release": "centos", "id": "sfo1", "description": "3/San Francisco 1"}, {"release": "centos", "id": "nyc3", "description": "8/New York 3"}, {"release": "amazon", "id": "ams2", "description": "5/Amsterdam 2"}, {"release": "centos", "id": "nyc2", "description": "4/New York 2"}, {"release": "amazon", "id": "sgp1", "description": "6/Singapore 1"}, {"release": "amazon", "id": "nyc2", "description": "4/New York 2"}, {"release": "amazon", "id": "ams3", "description": "9/Amsterdam 3"}, {"release": "amazon", "id": "nyc3", "description": "8/New York 3"}, {"release": "centos", "id": "lon1", "description": "7/London 1"}]'
MOCK_LOCATION_LIST_RELEASES_JSON = json.loads(MOCK_LOCATION_LIST_RELEASES_JSON_RAW)

MOCK_LOCATION_LIST_RELEASES_AMAZON_JSON_RAW = '[{"release": "amazon", "id": "lon1", "description": "7/London 1"}, {"release": "amazon", "id": "sfo1", "description": "3/San Francisco 1"}, {"release": "amazon", "id": "ams2", "description": "5/Amsterdam 2"}, {"release": "amazon", "id": "sgp1", "description": "6/Singapore 1"}, {"release": "amazon", "id": "nyc2", "description": "4/New York 2"}, {"release": "amazon", "id": "ams3", "description": "9/Amsterdam 3"}, {"release": "amazon", "id": "nyc3", "description": "8/New York 3"}]'
MOCK_LOCATION_LIST_RELEASES_AMAZON_JSON = json.loads(MOCK_LOCATION_LIST_RELEASES_AMAZON_JSON_RAW)

MOCK_HARDWARE_LIST_JSON_RAW = '[{"id":"512mb","processors":[{"cores":1.0,"speed":1.0}],"ram":512,"volumes":[{"type":"LOCAL","size":20.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"1gb","processors":[{"cores":1.0,"speed":1.0}],"ram":1024,"volumes":[{"type":"LOCAL","size":30.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"2gb","processors":[{"cores":2.0,"speed":2.0}],"ram":2048,"volumes":[{"type":"LOCAL","size":40.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"4gb","processors":[{"cores":2.0,"speed":2.0}],"ram":4096,"volumes":[{"type":"LOCAL","size":60.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"8gb","processors":[{"cores":4.0,"speed":4.0}],"ram":8192,"volumes":[{"type":"LOCAL","size":80.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"16gb","processors":[{"cores":8.0,"speed":8.0}],"ram":16384,"volumes":[{"type":"LOCAL","size":160.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"32gb","processors":[{"cores":12.0,"speed":12.0}],"ram":32768,"volumes":[{"type":"LOCAL","size":320.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"48gb","processors":[{"cores":16.0,"speed":16.0}],"ram":49152,"volumes":[{"type":"LOCAL","size":480.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}},{"id":"64gb","processors":[{"cores":20.0,"speed":20.0}],"ram":65536,"volumes":[{"type":"LOCAL","size":640.0,"bootDevice":false,"durable":false}],"providerZone":{"scope":"","id":"sfo1","description":"sfo1","iso3166Codes":[]}}]'
MOCK_HARDWARE_LIST_JSON = json.loads(MOCK_HARDWARE_LIST_JSON_RAW)

MOCK_INSTANCE_CREATE_TESTING_OK_JSON_RAW = '{"servername":"","ipv4":"1.2.3.4","id":"qse0hca2jj1di63k8bidvmffig","type":"testing","status":"Creating instance"}'
MOCK_INSTANCE_CREATE_TESTING_OK_JSON = json.loads(MOCK_INSTANCE_CREATE_TESTING_OK_JSON_RAW)

MOCK_INSTANCE_CREATE_PRODUCTION_OK_JSON_RAW = '{"servername":"","ipv4":"1.2.3.4","id":"s017frnl7ah6lqljkc4omt8h4k","type":"production","status":"Creating instance"}'
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

Please login in your account in %s and deploy a production server using the supplier manageacloud

You just need to make this action once.
''' % maccli.domain

OUTPUT_CONFIGURATION_LIST = '''
+---------------+-------------+---------+
| Tag           | Title       | Summary |
+---------------+-------------+---------+
| wordpress_128 | Wordpress   |         |
| test_server   | Test server |         |
+---------------+-------------+---------+

Search more at %s/cookbooks

''' % maccli.domain

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

Search more at %s/cookbooks

''' % maccli.domain

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

Search more at %s/cookbooks

''' % maccli.domain

OUTPUT_CREATE_INSTANCE_PRODUCTION_OK = '''+---------------+---------+----------------------------+------------+-------------------+
| Instance name |    IP   |        Instance ID         |    Type    |       Status      |
+---------------+---------+----------------------------+------------+-------------------+
|               | 1.2.3.4 | s017frnl7ah6lqljkc4omt8h4k | production | Creating instance |
+---------------+---------+----------------------------+------------+-------------------+

To monitor the creation progress:

watch mac instance list

'''

OUTPUT_CREATE_INSTANCE_TESTING_OK = '''+---------------+---------+----------------------------+---------+-------------------+
| Instance name |    IP   |        Instance ID         |   Type  |       Status      |
+---------------+---------+----------------------------+---------+-------------------+
|               | 1.2.3.4 | qse0hca2jj1di63k8bidvmffig | testing | Creating instance |
+---------------+---------+----------------------------+---------+-------------------+

To monitor the creation progress:

watch mac instance list

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

MOCK_MACFILE_ROOT = {'version': '1.0', 'name': 'manageacloud'}
MOCK_ONE_ROLE_ROLES = {'default': {'instance create': {'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': '104.236.167.158'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'name': '', 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}}}
MOCK_ONE_ROLE_INFRASTRUCTURES = {'default': {'amount': 1, 'role': 'default', 'location': 'sfo1', 'provider': 'manageacloud'}}
MOCK_ONE_ROLE_INSTANCE = {u'status': u'Creating instance', u'servername': u'', u'lifespan': 0, u'ipv4': u'', u'type': u'testing', u'id': u'kj5soodrvj4694thjd2o7cvcdc'}

MOCK_TWO_ROLE_ROLES = {'pgbench': {'instance create': {'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': 'postgres.PUBLIC_IP'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'name': '', 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}}, 'postgres': {'instance create': {'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}], 'name': '', 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'postgres_93_default'}}}
MOCK_TWO_ROLE_INFRASTRUCTURES = {'postgresinf': {'amount': 1, 'role': 'postgres', 'location': 'sfo1', 'provider': 'manageacloud'}, 'pgbenchinf': {'amount': 1, 'role': 'pgbench', 'location': 'sfo1', 'provider': 'manageacloud'}}
MOCK_TWO_ROLE_INSTANCE_POSTGRES = [{u'status': u'Creating instance', u'servername': u'', u'lifespan': 0, u'ipv4': u'', u'type': u'testing', u'id': u'kj5soodrvj4694thjd2o7cvcdc'}]

MOCK_PARSE_ENVS_ROLE = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': 'postgres.PUBLIC_IP'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_CLEAN = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': u'104.236.147.27'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_CREATED = {'postgres': [{u'status': u'Creating instance', u'servername': u'', u'lifespan': 0, u'ipv4': u'', u'type': u'testing', u'id': u'kj5soodrvj4694thjd2o7cvcdc'}]}
MOCK_CREDENTIALS = {u'ip': u'104.236.147.27', u'password': u'', u'privateKey': u'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAteCwNr184Aywxuh9ZIrRRztit8KqyaVUExPVuPM6wdOUTe25\n0ySnkB3dB4WgAyL0qgSYNQbWKdqxnA46P++PaXtTTFtYe3nQg7c+K6MRqwL8ijTE\n+sUMJOJxSF0JDaA76czeyVgeOzlfKSK34YFuquoFMf9ArXNkx1U2WjNJsYELOgvz\nVbjF17YriKTqH9s8TYwg19UIlw1Rh5YiA9bOEHbd0NcU9N3wwFpCACeyLnKUxf26\nqNFNxwZaTMz6vH5VLNSUL5A5bZA1aQ/mJLaVmdphky3xf6eScu1TbaYgvETaA97D\nggO0wnwzJW08JOAMNJpUAAZ8dSfexhz+jJnC+QIDAQABAoIBAEbEckwaVqhmx7Hd\nbEzepqdst/CAUiu7pIb3xMT9/vLD/ISF5zP8oyY0OHhgye3uf/xXZVHcoyAN8+Wg\ns5GFCOwmDDc9o6QHtdZKSmp4PLupodG0zqA0Y5FGeoWJjag7nJRQHq+BFeI9ZIWA\n+MNJtWHTRMo7Y1MZ/zCAO3HFWvsxbmonXnppWF2PRkYeZmp3rgqR0Kxd/tCrfX5D\nFEXED75xFnz80lAkxRJOUWFvK08cSWfII4RFK8nFHSeOoNvNopz3RRi0RqM5HjKP\niXBpda/ptfVBVvdkED7LHMrnVCDTjNmzGuMU/THgqg49UzPkyobYQFMYnwMyNNOZ\n11+dxAECgYEA6C6o0vNpdqrGgXK9LQt1jKLs0EP9oOrUsG941Plcu/Pxw7azmh8q\n80ErpgS1ARtzWHNl1saHJtLOLtJWOw+b56B+A0MjfXVK8ocsTwNH4ZN3lWfrSPi9\n8+ULQbjKcLz8hydGX9pDAXjCKzv+lMrTgX5E+KFgmU/z8Yn0WnttHVkCgYEAyIj6\n33kADUoDbFm5MQD6+/trXAAT2WkOSD/ndx3ozudiURiem5fToCQxV9aop7Hckzit\nOHM/wD5Mva7KWeS3t4f7eDox3vOTHHSa03yjxP9dUUJbjaecKREU/gJmW930nrSZ\nd7Y14BMDreQjQ8pob8VIt0FS8TO6NgVwNfE8/qECgYByVQetWU/Fr7Kwa9/cHphz\n+IbEx7ZNV1YEy9+kgGa55xZWWdF3Q4HS53Sm/Apl0S6rj6fGa1yCMax2Qf1UeAs9\ntDpZQOZpESkm5IldHzB2VDe+yr2B4XsobtFsO6L0gRuZMi3lZYU5ZE25HIHwozAj\nxBoSlOUMmeJ2PoilRcIlgQKBgEhAuotcMH2ZRkR6y3Pxk3zI6LS8PmqeJIw5oi9T\n8nbh/ZWUlkkfWhugDrtEV34cYooU6KynMbgVelb5rGTZOKyC7UMzTJa1EjM1fDdo\n+CTZkYjerNgMJQLS6cpfmPvOq/2muojceOrkTvYPdflN63UiEwIcIkNPzO775KM6\n6SwhAoGAeuaQUx4SWIIqdgPATxOJ/m5Ia49MqBzp14A7jbwDXO618koshlzcS04P\njim9FhSMpzWtgk+2kXQr3uBGTBJFZfn4DGVISMWupkWV3sCoZ94M1OW0Z5urWI1Y\n3gpqsDsitUIjTZq3b5xpMeOrGwk4aCq9wIxx/cFBBOD3Wh3pcKU=\n-----END RSA PRIVATE KEY-----\n', u'port': 22, u'user': u'root'}

MOCK_FACTS_PRIV_NETWORK = {u'kernel': u'Linux', u'domain': u'ec2.internal', u'puppetversion': u'3.4.3', u'ipaddress_lo': u'127.0.0.1', u'mtu_eth0': u'1500', u'memoryfree': u'493.71 MB', u'memorytotal': u'588.61 MB', u'swapfree': u'0.00 MB', u'augeasversion': u'1.2.0', u'is_virtual': u'true', u'timezone': u'UTC', u'hardwareisa': u'x86_64', u'sshfp_dsa': u'SSHFP 2 1 0929af91c3e78cea1082e0d296264e5ae8237a38\nSSHFP 2 2 9cf006e65020537a7bcda5ac5013efba740f2deaf046fe5bc58d1db0a20dbc02', u'id': u'root', u'netmask_lo': u'255.0.0.0', u'lsbmajdistrelease': u'14', u'memoryfree_mb': u'493.71', u'swapfree_mb': u'0.00', u'macaddress_eth0': u'12:6c:dd:b4:ae:18', u'rubyversion': u'1.9.3', u'hostname': u'ip-172-31-36-70', u'facterversion': u'1.7.5', u'lsbdistid': u'Ubuntu', u'virtual': u'xenu', u'operatingsystem': u'Ubuntu', u'blockdevices': u'xvda1,xvdm', u'sshfp_ecdsa': u'SSHFP 3 1 251628936ef6079c92be1797df934386740a851e\nSSHFP 3 2 b197de6a2946f8865b87ea565227ceedd4f3c6e89340af0a4e182e2f3db2078c', u'sshdsakey': u'AAAAB3NzaC1kc3MAAACBAJT0dIYETf5iqKr4bU30boyFtp1NXa7qGXY8E/YdhJ9PQiwqeOS4YQoYQTY+z+0HvHiAlZ45/Qjcm9QLR9E9D7bau5sAZN29Dh/wJDiiL4oa7Rfz/d1QaJw/KocETiYTk7Kl1FXSXmCNaUvi5/q8rQI+6/kySkXT5dyCZ3OTCz25AAAAFQCB4BBXRzq3AtgpJGZXAH9uD3EwoQAAAIA76F+ol/AW2ybVZZLGVKeBVqinP4WM3aqEqZC6lWVIF25mwnhA5FxnekjeBLWZiT/swHJNWpVo5e7x3Vn6vvDPr0DScUkg9zLhYWE13PIsZhMBNPMVDcgGMTmbv0BA7sI2i3JGqSoqjOS2+PB3IQA5OzmvnpfltIn83m/A63lbpgAAAIAaPbPNgSEPO6zHgu+STMFfzWOCtdg/9H1rsjiC5K6sJJgH4tLOgM/0+UMjxnN9h7470jnYf/6C0ZfPwxtcWx/DMCHcHLSvj5obZL+3lp5X1uEV++Nkfkh769O0/KyQVv2NdL+reRXDKWldmrIDX2EipsZ2Gp1zg54aNK6MhGcueg==', u'selinux': u'false', u'hardwaremodel': u'x86_64', u'uptime_seconds': 1964, u'rubysitedir': u'/usr/local/lib/site_ruby/1.9.1', u'ipaddress_eth0': u'172.31.36.70', u'blockdevice_xvdm_size': 107374182400, u'osfamily': u'Debian', u'sshrsakey': u'AAAAB3NzaC1yc2EAAAADAQABAAABAQCoWrR1rRc2BLOXNp/bzMaaSDCyA4QIS1SMu82m7GX3y7KUMq/0gJllGbmEDlZJ+bcVa1mBsFfl8q+ovC88s3D5BHLozKoFYVZlP5Gmmg7zpuKXGvU0HreMBQltl6PcbruGiVPYBvTKQxpYgso+w7dwrtayCXAhvbldVQTAR4kB+IxHPqnEaBSRBTGq5urY5dzHzgwET8WqiIa1PpABA4F6EOT9eLAtHQJzaBDg7rkIIKNgQ140nc08mEygDEf3UEqT88eLrF1ZsxAPwc3UwYf75T2pGfyGp4Rz509NuMfk0XQuX4il60Kk1asTZzgIO2W7hEfW0+JnOhM2EclKoKzP', u'sshfp_rsa': u'SSHFP 1 1 e0ac8a4475800a45f7ea55e3903840e1cff18380\nSSHFP 1 2 52a539b1b6394f3d1619bd035585620a54c825062bf9e203739d29ab20e34c60', u'ps': u'ps -ef', u'physicalprocessorcount': 1, u'interfaces': u'eth0,lo', u'swapsize_mb': u'0.00', u'memorysize': u'588.61 MB', u'uptime': u'0:32 hours', u'swapsize': u'0.00 MB', u'filesystems': u'ext2,ext3,ext4,iso9660,vfat', u'netmask': u'255.255.240.0', u'network_lo': u'127.0.0.0', u'uniqueid': u'1fac4624', u'kernelrelease': u'3.13.0-29-generic', u'path': u'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', u'blockdevice_xvda1_size': 8589934592, u'processorcount': u'1', u'ipaddress': u'172.31.36.70', u'lsbdistdescription': u'Ubuntu 14.04 LTS', u'mtu_lo': u'65536', u'kernelmajversion': u'3.13', u'kernelversion': u'3.13.0', u'macaddress': u'12:6c:dd:b4:ae:18', u'operatingsystemrelease': u'14.04', u'processor0': u'Intel(R) Xeon(R) CPU           E5645  @ 2.40GHz', u'network_eth0': u'172.31.32.0', u'uptime_days': 0, u'uptime_hours': 0, u'fqdn': u'ip-172-31-36-70.ec2.internal', u'lsbdistcodename': u'trusty', u'lsbdistrelease': u'14.04', u'memorysize_mb': u'588.61', u'sshecdsakey': u'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNHieMQZ5PRRvzNnCGs4HhXVdcylNgMck7mQ863UugS9nDBjxv5ARA692zDymsha7N0f2WMoshGxtOIoFfmglQc=', u'architecture': u'amd64', u'netmask_eth0': u'255.255.240.0'}
MOCK_FACTS_NOPRIV_NETWORK = {u'kernel': u'Linux', u'domain': u'ec2.internal', u'puppetversion': u'3.4.3', u'ipaddress_lo': u'127.0.0.1', u'mtu_eth0': u'1500', u'memoryfree': u'493.71 MB', u'memorytotal': u'588.61 MB', u'swapfree': u'0.00 MB', u'augeasversion': u'1.2.0', u'is_virtual': u'true', u'timezone': u'UTC', u'hardwareisa': u'x86_64', u'sshfp_dsa': u'SSHFP 2 1 0929af91c3e78cea1082e0d296264e5ae8237a38\nSSHFP 2 2 9cf006e65020537a7bcda5ac5013efba740f2deaf046fe5bc58d1db0a20dbc02', u'id': u'root', u'netmask_lo': u'255.0.0.0', u'lsbmajdistrelease': u'14', u'memoryfree_mb': u'493.71', u'swapfree_mb': u'0.00', u'macaddress_eth0': u'12:6c:dd:b4:ae:18', u'rubyversion': u'1.9.3', u'hostname': u'ip-172-31-36-70', u'facterversion': u'1.7.5', u'lsbdistid': u'Ubuntu', u'virtual': u'xenu', u'operatingsystem': u'Ubuntu', u'blockdevices': u'xvda1,xvdm', u'sshfp_ecdsa': u'SSHFP 3 1 251628936ef6079c92be1797df934386740a851e\nSSHFP 3 2 b197de6a2946f8865b87ea565227ceedd4f3c6e89340af0a4e182e2f3db2078c', u'sshdsakey': u'AAAAB3NzaC1kc3MAAACBAJT0dIYETf5iqKr4bU30boyFtp1NXa7qGXY8E/YdhJ9PQiwqeOS4YQoYQTY+z+0HvHiAlZ45/Qjcm9QLR9E9D7bau5sAZN29Dh/wJDiiL4oa7Rfz/d1QaJw/KocETiYTk7Kl1FXSXmCNaUvi5/q8rQI+6/kySkXT5dyCZ3OTCz25AAAAFQCB4BBXRzq3AtgpJGZXAH9uD3EwoQAAAIA76F+ol/AW2ybVZZLGVKeBVqinP4WM3aqEqZC6lWVIF25mwnhA5FxnekjeBLWZiT/swHJNWpVo5e7x3Vn6vvDPr0DScUkg9zLhYWE13PIsZhMBNPMVDcgGMTmbv0BA7sI2i3JGqSoqjOS2+PB3IQA5OzmvnpfltIn83m/A63lbpgAAAIAaPbPNgSEPO6zHgu+STMFfzWOCtdg/9H1rsjiC5K6sJJgH4tLOgM/0+UMjxnN9h7470jnYf/6C0ZfPwxtcWx/DMCHcHLSvj5obZL+3lp5X1uEV++Nkfkh769O0/KyQVv2NdL+reRXDKWldmrIDX2EipsZ2Gp1zg54aNK6MhGcueg==', u'selinux': u'false', u'hardwaremodel': u'x86_64', u'uptime_seconds': 1964, u'rubysitedir': u'/usr/local/lib/site_ruby/1.9.1', u'ipaddress_eth0': u'1.2.3.4', u'blockdevice_xvdm_size': 107374182400, u'osfamily': u'Debian', u'sshrsakey': u'AAAAB3NzaC1yc2EAAAADAQABAAABAQCoWrR1rRc2BLOXNp/bzMaaSDCyA4QIS1SMu82m7GX3y7KUMq/0gJllGbmEDlZJ+bcVa1mBsFfl8q+ovC88s3D5BHLozKoFYVZlP5Gmmg7zpuKXGvU0HreMBQltl6PcbruGiVPYBvTKQxpYgso+w7dwrtayCXAhvbldVQTAR4kB+IxHPqnEaBSRBTGq5urY5dzHzgwET8WqiIa1PpABA4F6EOT9eLAtHQJzaBDg7rkIIKNgQ140nc08mEygDEf3UEqT88eLrF1ZsxAPwc3UwYf75T2pGfyGp4Rz509NuMfk0XQuX4il60Kk1asTZzgIO2W7hEfW0+JnOhM2EclKoKzP', u'sshfp_rsa': u'SSHFP 1 1 e0ac8a4475800a45f7ea55e3903840e1cff18380\nSSHFP 1 2 52a539b1b6394f3d1619bd035585620a54c825062bf9e203739d29ab20e34c60', u'ps': u'ps -ef', u'physicalprocessorcount': 1, u'interfaces': u'eth0,lo', u'swapsize_mb': u'0.00', u'memorysize': u'588.61 MB', u'uptime': u'0:32 hours', u'swapsize': u'0.00 MB', u'filesystems': u'ext2,ext3,ext4,iso9660,vfat', u'netmask': u'255.255.240.0', u'network_lo': u'127.0.0.0', u'uniqueid': u'1fac4624', u'kernelrelease': u'3.13.0-29-generic', u'path': u'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', u'blockdevice_xvda1_size': 8589934592, u'processorcount': u'1', u'ipaddress': u'172.31.36.70', u'lsbdistdescription': u'Ubuntu 14.04 LTS', u'mtu_lo': u'65536', u'kernelmajversion': u'3.13', u'kernelversion': u'3.13.0', u'macaddress': u'12:6c:dd:b4:ae:18', u'operatingsystemrelease': u'14.04', u'processor0': u'Intel(R) Xeon(R) CPU           E5645  @ 2.40GHz', u'network_eth0': u'172.31.32.0', u'uptime_days': 0, u'uptime_hours': 0, u'fqdn': u'ip-172-31-36-70.ec2.internal', u'lsbdistcodename': u'trusty', u'lsbdistrelease': u'14.04', u'memorysize_mb': u'588.61', u'sshecdsakey': u'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNHieMQZ5PRRvzNnCGs4HhXVdcylNgMck7mQ863UugS9nDBjxv5ARA692zDymsha7N0f2WMoshGxtOIoFfmglQc=', u'architecture': u'amd64', u'netmask_eth0': u'255.255.240.0'}
MOCK_PARSE_ENVS_NO_ROLE = {'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': 'postgres.PUBLIC_IP'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'name': '', 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_NO_ROLE_CREATED = {}
MOCK_PARSE_ENVS_ROLE_PRIV = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': 'postgres.PRIVATE_IP'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_FACT = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': 'postgres.FACT.kernel'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_PRIV_CLEAN = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': u'172.31.36.70'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_NOPRIV_CLEAN = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': u'1.2.3.4'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}
MOCK_PARSE_ENVS_ROLE_FACT_CLEAN = {'name': '', 'environment': [{'DBNAME': 'pgbench'}, {'PGUSER': 'benchuser'}, {'IP': u'Linux'}, {'BENCH_CREATION': '-i -s 70'}, {'BENCH_TEST': '-c 4 -j 2 -T 10'}], 'branch': 'master', 'deployment': 'testing', 'release': 'any', 'configuration': 'pgbench'}

MOCK_PARSE_MACFILE_AWS_ROLE = OrderedDict([('postgres', OrderedDict([('instance create', OrderedDict([('branch', 'master'), ('configuration', 'postgres_93_default'), ('environment', [OrderedDict([('DBNAME', 'pgbench')]), OrderedDict([('PGUSER', 'benchuser')])])]))])),
                                           ('pgbench', OrderedDict([('instance create', OrderedDict([('branch', 'master'), ('configuration', 'pgbench'), ('environment', [OrderedDict([('DBNAME', 'pgbench')]), OrderedDict([('PGUSER', 'benchuser')]), OrderedDict([('IP', 'postgres.PUBLIC_IP')]), OrderedDict([('BENCH_CREATION', '-i -s 70')]), OrderedDict([('BENCH_TEST', '-c 4 -j 2 -T 10')])])]))]))])

MOCK_PARSE_MACFILE_AWS_INF  = OrderedDict([('postgres', OrderedDict([('hardware', 'm3.medium'), ('location', 'us-east-1'), ('provider', 'amazon'), ('role', 'postgres'), ('deployment', 'testing'), ('name', ''), ('release', 'any'), ('amount', 1)])),
                                           ('pgbench', OrderedDict([('hardware', 'm3.medium'), ('location', 'us-east-1'), ('provider', 'amazon'), ('deployment', 'testing'), ('name', ''), ('release', 'any'), ('role', 'pgbench'), ('amount', 1)]))])

MOCK_PARSE_MACFILE_AWS_NO_ORDER_INF  = OrderedDict([('postgres', OrderedDict([('location', 'us-east-1'), ('hardware', 'm3.medium'), ('provider', 'amazon'), ('role', 'postgres'), ('amount', 1), ('name', ''), ('release', 'any'), ('deployment', 'testing')])),
                                                    ('pgbench', OrderedDict([('hardware', 'm3.medium'), ('location', 'us-east-1'), ('provider', 'amazon'), ('role', 'pgbench'), ('amount', 1), ('name', ''), ('release', 'any'), ('deployment', 'testing')]))])

MOCK_PARSE_ENVS_NO_ENVIRONMENT_ROLE_RAW = OrderedDict([('default', OrderedDict([('instance create', OrderedDict([('branch', 'master'), ('configuration', 'postgres_93_customized')]))]))])
MOCK_PARSE_ENVS_EMPTY_ROLES_CREATED = {}

MOCK_PARSE_MACFILE_V2_EXPECTED_ROOT = {'version': '1.0', 'name': 'demo'}
MOCK_PARSE_MACFILE_V2_EXPECTED_ROLES = OrderedDict([('app', OrderedDict([('instance create', OrderedDict([('configuration', 'demo_application'), ('environment', [OrderedDict([('DB_IP', '127.0.0.1')]), OrderedDict([('APP_BRANCH', 'master')])])]))]))])
MOCK_PARSE_MACFILE_V2_EXPECTED_INFRASTRUCTURES = OrderedDict([('app_inf', OrderedDict([('name', 'app'), ('provider', 'amazon'), ('location', 'us-east-1'), ('hardware', 't1.micro'), ('role', 'app')])), ('build_lb_inf', OrderedDict([('resource', 'build_lb')])), ('register_lb_inf', OrderedDict([('resource', 'register_lb')]))])
MOCK_PARSE_MACFILE_V2_EXPECTED_ACTIONS = OrderedDict([('get_id', OrderedDict([('ssh', 'wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')]))])
MOCK_PARSE_MACFILE_V2_1_EXPECTED_ACTIONS = OrderedDict([('get_id', OrderedDict([('ssh', 'wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')])), ('get_availability_zone', OrderedDict([('ssh', 'wget -q -O - http://169.254.169.254/latest/meta-data/placement/availability-zone')]))])
MOCK_PARSE_MACFILE_V2_EXPECTED_RESOURCES = OrderedDict([('build_lb', OrderedDict([('create bash', 'aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --region us-east-1 --availability-zones us-east-1e us-east-1b us-east-1c')])), ('register_lb', OrderedDict([('create bash', 'aws elb register-instances-with-load-balancer --load-balancer-name my-load-balancer --instances role.app.get_id --region us-east-1')]))])

AWS_DESCRIBE_ROUTE_RAW = '{"RouteTables": [ { "Associations": [ { "RouteTableAssociationId": "rtbassoc-44d2b020", "Main": true, "RouteTableId": "rtb-147bde70" } ], "RouteTableId": "rtb-147bde70", "VpcId": "vpc-6b51a10f", "PropagatingVgws": [], "Tags": [], "Routes": [  { "GatewayId": "local", "DestinationCidrBlock": "10.0.0.0/16", "State": "active", "Origin": "CreateRouteTable"  }]}]}'