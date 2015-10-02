import re
import argparse
from maccli.config import MACFILE_ON_FAILURE_DESTROY_ALL, MACFILE_ON_FAILURE_DESTROY_OTHERS


def add_login_parser(subparsers):
    subparsers.add_parser('login', help='Login into Manageacloud.com', description='Login into Manageacloud.com')


def add_instance_parser(subparsers):
    instance_parser = subparsers.add_parser('instance', help='Instance related operations',
                                            description='Server instances operations')

    instance_subparser = instance_parser.add_subparsers(title='mac instance commands', dest='subcmd')

    # list instance
    list_parser = instance_subparser.add_parser('list',
                                                help='List testing and production server instances',
                                                description='List testing and production server instances available in your account')

    # create instance
    create_parser = instance_subparser.add_parser('create', help='Create a new instance',
                                                  description='Creates a new instance in the cloud. You need to choose the '
                                                              'configuration that you want to apply. Please note that '
                                                              'you can create testing servers, which have a limited lifespan, '
                                                              'and production servers, '
                                                              'that must be destroyed manually.')

    create_parser.add_argument('-c', '--configuration', help='Configuration tag')

    create_parser.add_argument('-l', '--location',
                               help='Location name. If no provided, the list of available locations will be displayed.')

    create_parser.add_argument('-d', '--deployment', default="testing", choices=["testing", "production"],
                               help="Choose the type of server. Testing servers will has a limited lifespan (default is 'testing')")

    create_parser.add_argument('-b', '--branch', default="master", choices=["development", "master"],
                               help="Select the branch. This only applies if the provider is 'manageacloud'. "
                                    "(default is 'master')")

    create_parser.add_argument('-p', '--provider', default="manageacloud",
                               choices=["manageacloud", "rackspaceus", "rackspaceuk", "amazon", "digitalocean", "gce"],
                               help="Select the public cloud provider. (default is 'manageacloud')")

    create_parser.add_argument('-n', '--name',
                               help='Server name (default will be a random name)')

    create_parser.add_argument('-r', '--release', default="any",
                               choices=["any", "ubuntu", "centos", "debian", "amazon"],
                               help="Choose the distribution (default is 'any', which is the "
                                    "best match for 'configuration' parameter)")

    create_parser.add_argument('-hw', '--hardware',
                               help="Choose the hardware settings. It only applies if parameter 'deployment' is 'production'. "
                                    "If this parameter is not set, the list of the available hardware will be displayed.")

    create_parser.add_argument('-t', '--lifespan', type=int,
                               help="If deployment is 'development' choose the lifespan of the server. "
                                    "In minutes (default 90)")

    create_parser.add_argument('-e', '--environment', nargs='*', type=validate_environment,
                               help="Format KEY=VALUE. The environment variables will be available"
                                    " in the bootstrap bash script that applies the changes.")

    create_parser.add_argument('-hd', nargs='*', type=validate_hd,
                               help="For provider amazon: Format NAME:SIZE[:TYPE[:VALUE]] "
                                    "where NAME is the name of the device (example '/dev/sdb'), "
                                    "SIZE is a number in gigabytes, TYPE is the volume type (io1, gp2 or standard)"
                                    " and VALUE is the IOPS required if volume type is io1. \n"
                                    "For provider gce: NAME:SIZE:TYPE. NAME is the name of the device "
                                    "('testing' will be '/dev/disk/by-id/google-testing'), SIZE is the size "
                                    "in gigabytes and TYPE is 'ssd' or 'standard'. For rackspace: Format "
                                    "NAME:SIZE[:TYPE] where NAME is the name of the device (example '/dev/sdb')"
                                    " SIZE is the size in gb (min 100) and TYPE is 'SSD' or 'SATA'")

    create_parser.add_argument('--port', type=validate_port,
                               help="List of ports that are opened. "
                                    "The port 22 (SSH) must be in the list. "
                                    "Example: 22,80,8020")

    create_parser.add_argument('--net',
                               help="Network related property. For provider 'amazon', VPC subnet id. ")


    create_parser.add_argument('-y', '--yaml', action='store_true', default=False,
                               help="Prints the equivalent command in Macfile and exits.")

    # update instance
    update_parser = instance_subparser.add_parser('update',
                                                   help='Run the server configuration',
                                                   description='Run the server configuration')
    update_parser.add_argument('id', nargs='*',
                                help="Server ID or server name. It also accepts several values. If value is 'all' it applies to all servers.")

    update_parser.add_argument('-c', '--configuration', help='Configuration tag')

    # destroy instance
    destroy_parser = instance_subparser.add_parser('destroy',
                                                   help='Destroy an existing instance',
                                                   description='Destroy an existing instance')

    destroy_parser.add_argument('id', nargs='*',
                                help='Server ID or server name')

    # ssh instance
    ssh_parser = instance_subparser.add_parser('ssh',
                                       help='Connect via SSH',
                                       description='Connect via SSH to the server')

    ssh_parser.add_argument('id', nargs='*',
                            help="Server ID or server name. It also accepts several values. If value is 'all' it applies to all servers.")

    ssh_parser.add_argument('-c', '--command', nargs=argparse.REMAINDER, help='Run a command and exit')

    # facts instance
    facts_parser = instance_subparser.add_parser('facts',
                                                 help='Retrieves facts about an instance',
                                                 description='Retrieves facts about  an instance')
    facts_parser.add_argument('id', help='Server ID or server name')

    # logs
    logs_parser = instance_subparser.add_parser('log',
                                                help='Show instance logs',
                                                description='Show server output when creating and applying '
                                                            'the configuration to an instance')

    logs_parser.add_argument('id', help='Server ID or server name')

    # lifespan operations
    lifespan_parser = instance_subparser.add_parser('lifespan',
                                                    help='Manipulate testing instance\'s lifespan',
                                                    description='Add or remove testing instance lifespan')
    lifespan_parser.add_argument('id', help='Server ID or server name')
    lifespan_parser.add_argument('amount', type=int, help='New server lifespan in minutes')


def add_infrastructure_parser(subparsers):
    """ infrastructure parser"""
    inf_parser = subparsers.add_parser('infrastructure',
                                       help='Infrastructure operations',
                                       description='Infrastructure related operations')

    inf_subparser = inf_parser.add_subparsers(title='infrastructure operations', dest='subcmd')

    # infrastructure macfile
    macfile_parser = inf_subparser.add_parser('macfile', help='Create an infrastructure',
                                              description='Create an infrastructure loading a macfile')

    # get file path
    macfile_parser.add_argument('file', nargs=1, help='Path to Macfile')
    macfile_parser.add_argument('--resume', action='store_true', help="Resume infrastructure creation")
    macfile_parser.add_argument('-p', '--param', nargs='*', help="Add parameters to be replaced in the macfile")
    macfile_parser.add_argument('--on_failure', choices=[MACFILE_ON_FAILURE_DESTROY_ALL, MACFILE_ON_FAILURE_DESTROY_OTHERS],
                                help="Action to be taken a server fails. 'destroy_all' "
                                     "will completely remove every server created. "
                                     "To allow debugging, 'destroy_others' will destroy "
                                     "all the servers that did not fail (this allows to debug)")

    # infrastructure list
    inf_subparser.add_parser('list', help='List all infrastructure and versions available')

    # infrastructure instance
    instance_parser = inf_subparser.add_parser('items', help='List instances and resources available in a infrastructure')
    instance_parser.add_argument('-v', '--version', help='Filter by infrastructure version')
    instance_parser.add_argument('-n', '--name', help='Filter by infrastructure name')

    # infrastructure destroy
    instance_parser = inf_subparser.add_parser('destroy', help='Destroy instances and resources')
    instance_parser.add_argument('name', help='Infrastructure name')
    instance_parser.add_argument('version', help='Infrastructure version')

    # infrastructure update
    instance_parser = inf_subparser.add_parser('update', help='Update instance configuration')
    instance_parser.add_argument('name', help='Infrastructure name')
    instance_parser.add_argument('version', help='Infrastructure version')
    instance_parser.add_argument('-c', '--configuration', help='Configuration tag')

    # lifespan
    lifespan_parser = inf_subparser.add_parser('lifespan', help='Manipulate testing instance\'s lifespan')
    lifespan_parser.add_argument('amount', type=int, help='New server lifespan in minutes')
    lifespan_parser.add_argument('-v', '--version', help='Filter by infrastructure version')
    lifespan_parser.add_argument('-n', '--name', help='Filter by infrastructure name')


def add_configuration_parser(subparsers):
    configuration_parser = subparsers.add_parser('configuration', help='Server configuration related operations',
                                                 description='Search public and private configurations')

    configuration_subparser = configuration_parser.add_subparsers(title='mac configuration commands', dest='subcmd')

    # list instance
    list_parser = configuration_subparser.add_parser('list',
                                                     help='List your server configurations',
                                                     description='List the server configurations available in your account')

    search_parser = configuration_subparser.add_parser('search',
                                                       help='Search public server configurations',
                                                       description='Search public server configurations available in Manageacloud.com')

    search_parser.add_argument('-k', '--keyword',
                               help='Keywords', nargs='*')

    search_parser.add_argument('-u', '--url',
                               help='Show Urls', action='store_true', default=False)


def validate_environment(input):
    """
        Checks that the input parameter has the format
        KEY=VALUE
    """
    a = re.compile("^[A-Z0-9\_\-]+\=.+$", re.IGNORECASE)
    match = a.match(input)
    if not match:
        msg = "'%s' environment contains invalid characters or the format KEY=VALUE is not correct" % input
        raise argparse.ArgumentTypeError(msg)
    key, value = input.split("=", 1)
    to_return = {key: value}
    return to_return


def validate_hd(input):
    """
        checks that the input
        /dev/name:SIZE[:type[:value]] is correct./
    """
    a = re.compile("^[/a-zA-Z1-9]+:[0-9]+(:[a-zA-Z0-9]+(:[a-zA-Z0-9]+)?)?$", re.IGNORECASE)
    match = a.match(input)
    if not match:
        msg = "'%s' hard-disk is invalid. Correct value NAME:SIZE<:TYPE<:VALUE>> name are letters and " \
              "number and SIZE is a number that represents the gigabytes." % input
        raise argparse.ArgumentTypeError(msg)
    key, value = input.split(":", 1)
    to_return = {key: value}
    return to_return


def validate_port(port_input):
    """
        checks that the input 22,80,2020 is correct
    """
    ports_raw = port_input.split(',')
    ports = []
    ssh_port = False
    for port_raw in ports_raw:
        try:
            port = int(port_raw)
            if port == 22:
                ssh_port = True
            if port < 1 or port > 65535:
                msg = "'%s' doesn't look valid. The value %s should be between 1 and 65535" % (port_raw, port_input)
                raise argparse.ArgumentTypeError(msg)

        except ValueError:
            msg = "'%s' doesn't look valid. The value %s is not an integer" % (port_raw, port_input)
            raise argparse.ArgumentTypeError(msg)
        ports.append(port)

    if not ssh_port:
        msg = "'%s' doesn't look valid. You need to allow access to the port 22" % port_input
        raise argparse.ArgumentTypeError(msg)

    return ports
