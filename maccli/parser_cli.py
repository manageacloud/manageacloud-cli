import re
import argparse

def add_login_parser(subparsers):
    subparsers.add_parser('login', help='Login into Manageacloud.com', description='Login into Manageacloud.com')

def add_instance_parser(subparsers):
    instance_parser = subparsers.add_parser('instance', help='Manage testing or production server instances',
                                            description='Create, destroy, search or list server instances')

    instance_subparser = instance_parser.add_subparsers(title='mac instance commands', dest='subcmd')

    # list instance
    list_parser = instance_subparser.add_parser('list',
                                                help='List testing and production server instances',
                                                description='List testing and production server instances available in your account')

    # ssh instance
    ssh_parser = instance_subparser.add_parser('ssh',
                                               help='Connect via SSH',
                                               description='Connect via SSH to the server')

    ssh_parser.add_argument('-n', '--name', help='Server name')

    ssh_parser.add_argument('-i', '--id', help='Server ID')

    ssh_parser.add_argument('-c', '--command', help='Run a command and exit')

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
                               choices=["manageacloud", "rackspaceus", "amazon", "digitalocean", "gce"],
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

    create_parser.add_argument('-t', '--lifespan', type=int, help="If deployment is 'development' choose the lifespan of the server. "
                                                        "In minutes (default 90)" )

    create_parser.add_argument('-e', '--environment', nargs='*', type=validate_environment,
                               help="Format KEY=VALUE. The environment variables will be available"
                                    " in the bootstrap bash script that applies the changes." )

    create_parser.add_argument('-hd', nargs='*', type=validate_hd,
                               help="Format /dev/name:SIZE where /dev/name is the name "
                                    "of the device (example '/dev/sda') and SIZE is a number"
                                    "that represents gigabytes. Supported providers: amazon")

    create_parser.add_argument('-y', '--yaml', action='store_true', default=False,
                               help="Prints the equivalent command in Macfile and exits.")




    # destroy instance
    destroy_parser = instance_subparser.add_parser('destroy',
                                                   help='Destroy an existing instance',
                                                   description='Destroy an existing instance')

    destroy_parser.add_argument('-n', '--name',
                                help='Server name')

    destroy_parser.add_argument('-i', '--id',
                                help='Server ID')

    # facts instance
    facts_parser = instance_subparser.add_parser('facts',
                                                help='Retrieves facts about the system',
                                                description='Retrieves facts about the system')
    facts_parser.add_argument('-n', '--name',
                                help='Server name')

    facts_parser.add_argument('-i', '--id',
                                help='Server ID')




def add_configuration_parser(subparsers):
    configuration_parser = subparsers.add_parser('configuration', help='Manage configurations',
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


def add_macfile_parser(subparsers):

    macfile_parser = subparsers.add_parser('macfile', help='Load a Macfile', description='Load a Macfile and execute its contents')

    # get file path
    file_parser = macfile_parser.add_argument('file',
                                              nargs = 1,
                                              help='Path to Macfile')


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
    to_return = {key:value}
    return to_return

def validate_hd(input):
    """
        checks that the input
        /dev/name:SIZE[:type] is correct./
    """
    a = re.compile("^/dev/[a-zA-Z1-9]+:[0-9]+(:[a-zA-Z0-9]+(:[a-zA-Z0-9]+)?)?$", re.IGNORECASE)
    match = a.match(input)
    if not match:
        msg = "'%s' hard-disk is invalid. Correct value /dev/<name>:<SIZE>, name are letters and " \
              "number and SIZE is a number that represents the gigabytes." % input
        raise argparse.ArgumentTypeError(msg)
    key, value = input.split(":", 1)
    to_return = {key:value}
    return to_return

