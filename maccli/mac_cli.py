import sys
import logging
import codecs
import copy
import argparse

import maccli
import parser_cli
import maccli.command_cli

from maccli.helper.exception import InternalError
from maccli.view.view_generic import show_error


sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def initialize_parser():
    # Top parser
    parser = argparse.ArgumentParser(description="Manageacloud.com CLI", prog='mac')
    parser.add_argument('--version', action='version', version='%(prog)s ' + maccli.__version__)
    parser.add_argument('-v', '--verbose', action='store_true', help="Show verbose information")
    parser.add_argument('-q', '--quiet', action='store_true', help="Enable loggable output")
    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(title="mac's CLI commands", dest='cmd')
    parser_cli.add_login_parser(subparsers)
    parser_cli.add_instance_parser(subparsers)
    parser_cli.add_configuration_parser(subparsers)
    parser_cli.add_infrastructure_parser(subparsers)
    return parser


def patch_help_option(argv=sys.argv):
    args = copy.copy(argv)

    if not args:
        raise InternalError("Wrong argument is set, cannot be empty")

    if len(args) == 1:
        maccli.command_cli.help()

    if len(args) == 2:
        if args[1] == 'instance':
            maccli.command_cli.instance_help()

        if args[1] == 'configuration':
            maccli.command_cli.configuration_help()

    return args[1:]


def dispatch_cmds(args):

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    maccli.quiet = args.quiet

    maccli.logger.debug("Args options %s: " % args)

    if args.cmd == 'login':
        maccli.command_cli.login()

    elif maccli.user is None:
        maccli.command_cli.no_credentials()

    elif args.cmd == 'instance':

        if args.subcmd == 'create':
            if args.yaml:
                maccli.command_cli.convert_to_yaml(args)
            else:
                maccli.command_cli.instance_create(args.configuration, args.deployment, args.location, args.name,
                                                   args.provider, args.release, args.branch, args.hardware, args.lifespan,
                                                   args.environment, args.hd, args.net, args.port)
        elif args.subcmd == 'update':
            if args.id is None:
                show_error("Parameter 'id' is required.")
                maccli.command_cli.instance_update_help()
            else:
                maccli.command_cli.instance_update(args.id)

        elif args.subcmd == 'destroy':
            if args.id is None:
                show_error("Parameter 'id' is required.")
                maccli.command_cli.instance_destroy_help()
            else:
                maccli.command_cli.instance_destroy(args.id)

        elif args.subcmd == 'list':
            maccli.command_cli.instance_list()

        elif args.subcmd == 'facts':
            maccli.command_cli.instance_fact(args.id)

        elif args.subcmd == 'log':
            maccli.command_cli.instance_log(args.id)

        elif args.subcmd == 'lifespan':
            maccli.command_cli.instance_lifespan(args.id, args.amount)

        elif args.subcmd == 'ssh':
            if args.id is None:
                show_error("Parameter 'id' is required.")
                maccli.command_cli.instance_ssh_help()
            else:
                if args.command is not None:
                    command = " ".join(args.command)
                else:
                    command = args.command

                maccli.command_cli.instance_ssh(args.id, command)

    elif args.cmd == "configuration":
        if args.subcmd == 'list':
            maccli.command_cli.configuration_list()
        elif args.subcmd == 'search':
            maccli.command_cli.configuration_search(args.keyword, args.url)

    elif args.cmd == "infrastructure":
        if args.subcmd == 'list':
            maccli.command_cli.infrastructure_list()
        elif args.subcmd == 'macfile':
            maccli.command_cli.process_macfile(args.file[0], args.resume, args.param, args.quiet, args.on_failure)
        elif args.subcmd == 'items':
            maccli.command_cli.infrastructure_search(args.name, args.version)
        elif args.subcmd == 'destroy':
            maccli.command_cli.infrastructure_destroy(args.name, args.version)

        elif args.subcmd == 'lifespan':
            maccli.command_cli.infrastructure_lifespan(args.amount, args.name, args.version)


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