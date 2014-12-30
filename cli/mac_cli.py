import sys, logging, codecs, copy
import argparse
import mac, parser_cli, command_cli
from exception_cli import InternalError

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
logging.basicConfig()


def initialize_parser():
    # Top parser
    parser = argparse.ArgumentParser(description="Manageacloud.com CLI", prog='mac')
    parser.add_argument('--version', action='version', version='%(prog)s ' + mac.__version__)
    # parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(title="mac's CLI commands", dest='cmd')
    parser_cli.add_login_parser(subparsers)
    parser_cli.add_instance_parser(subparsers)
    return parser


def patch_help_option(argv=sys.argv):
    args = copy.copy(argv)

    if not args:
        raise InternalError("Wrong argument is set, cannot be empty")

    return args[1:]


def dispatch_cmds(args):

    if args.cmd == 'login':
        command_cli.login()

    if args.cmd == 'instance':
        if args.subcmd == 'create':
            command_cli.instance_create()
        elif args.subcmd == 'destroy':
            command_cli.instance_destroy()
        elif args.subcmd == 'list':
            command_cli.instance_list()


def parse_args(self, args):
    # factored out for testability
    return self.parser.parse_args(args)


def main():
    parser = initialize_parser()
    argv = patch_help_option(sys.argv)
    args = parser.parse_args(argv)
    dispatch_cmds(args)

if __name__ == "__main__":
    main()