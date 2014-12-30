def add_login_parser(subparsers):
    subparsers.add_parser('login', help='Login into Manageacloud.com', description='Login into Manageacloud.com')


def add_instance_parser(subparsers):
    instance_parser = subparsers.add_parser('instance', help='Manage testing or production server instances',
                                                 description='Create, destroy, search or list server instances')

    instance_parser.add_argument('create', help='Create a new testing or production server instance')
    instance_parser.add_argument('destroy', help='Destroy a server instance')
    instance_parser.add_argument('list', help='List testing and production server instances available in your account')