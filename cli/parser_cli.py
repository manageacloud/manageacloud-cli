def add_login_parser(subparsers):
    subparsers.add_parser('login', help='Login into Manageacloud.com', description='Login into Manageacloud.com')


def add_instance_parser(subparsers):
    instance_parser = subparsers.add_parser('instance', help='Manage testing or production server instances',
                                            description='Create, destroy, search or list server instances')

    instance_subparser = instance_parser.add_subparsers(title='mac instance commands', dest='subcmd')

    # list instance
    list_parser = instance_subparser.add_parser('list',
                                                help='List testing and production server instances available in your account',
                                                description='List testing and production server instances available in your account')

    # create instance
    create_parser = instance_subparser.add_parser('create', help='Create a new service',
                                                  description='Create a new service', )


    # destroy instance
    destroy_parser = instance_subparser.add_parser('destroy', help='Destroy a server instance',
                                                   description='Destroy a server instance')




