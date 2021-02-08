import sys
import logging
import codecs
import copy
import argparse

import maccli
import maccli.parser_cli
import maccli.command_cli
#import maccli.lib.
#from maccli.lib.aliases import AliasedSubParsersAction
#import maccli.interactive

from maccli.helper.exception import InternalError
from maccli.view.view_generic import show_error


# TODO lib aliases is kind of failing ... not sure why
class AliasedSubParsersAction(argparse._SubParsersAction):
    old_init = staticmethod(argparse._ActionsContainer.__init__)

    @staticmethod
    def _containerInit(self, description, prefix_chars, argument_default, conflict_handler):
        AliasedSubParsersAction.old_init(self, description, prefix_chars, argument_default, conflict_handler)
        self.register('action', 'parsers', AliasedSubParsersAction)

    class _AliasedPseudoAction(argparse.Action):
        def __init__(self, name, aliases, help):
            dest = name
            if aliases:
                dest += ' (%s)' % ','.join(aliases)
            sup = super(AliasedSubParsersAction._AliasedPseudoAction, self)
            sup.__init__(option_strings=[], dest=dest, help=help)

    def add_parser(self, name, **kwargs):
        aliases = kwargs.pop('aliases', [])
        parser = super(AliasedSubParsersAction, self).add_parser(name, **kwargs)

        # Make the aliases work.
        for alias in aliases:
            self._name_parser_map[alias] = parser
        # Make the help text reflect them, first removing old help entry.
        if 'help' in kwargs:
            help = kwargs.pop('help')
            self._choices_actions.pop()
            pseudo_action = self._AliasedPseudoAction(name, aliases, help)
            self._choices_actions.append(pseudo_action)

        return parser



def initialize_parser():
    # Top parser
    parser = argparse.ArgumentParser(description="Manageacloud.com CLI", prog='mac')
    parser.register('action', 'parsers', AliasedSubParsersAction)
    parser.add_argument('--version', action='version', version='%(prog)s ' + maccli.__version__)
    parser.add_argument('-v', '--verbose', action='store_true', help="Show verbose information")
    parser.add_argument('-q', '--quiet', action='store_true', help="Enable loggable output")
    parser.add_argument('-s', '--disable-strict-host', action='store_true', help="Disable Strict Host Key Checking. It sets the SSH parameter -o 'StrictHostKeyChecking no' when connecting to the instances.")
    parser.add_argument('--debug', action='store_true', help="Enable debug")
    #parser.add_argument('-i', '--interactive', action='store_true', dest="interactive", help="Interactive session - preview feature")
    subparsers = parser.add_subparsers(title="mac's CLI commands", dest='cmd')
    maccli.parser_cli.add_login_parser(subparsers)
    maccli.parser_cli.add_instance_parser(subparsers)
    maccli.parser_cli.add_resource_parser(subparsers)
    maccli.parser_cli.add_configuration_parser(subparsers)
    maccli.parser_cli.add_infrastructure_parser(subparsers)
    maccli.parser_cli.add_provider_parser(subparsers)
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

        if args[1] == 'provider':
            maccli.command_cli.provider_help()

    return args[1:]


def dispatch_cmds(args):

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    maccli.quiet = args.quiet
    maccli.disable_strict_host_check = args.disable_strict_host

    maccli.logger.debug("Args options %s: " % args)

    if args.cmd == 'login':
        maccli.command_cli.login()

    elif maccli.user is None:
        maccli.command_cli.no_credentials()

    elif args.cmd == 'instance' or args.cmd == 'ins':

        if args.subcmd == 'create':
            if args.yaml:
                maccli.command_cli.convert_to_yaml(args)
            else:
                maccli.command_cli.instance_create(args.configuration, args.bootstrap, args.deployment, args.location, args.name,
                                                   #args.provider, args.release, args.release_version, args.branch, args.hardware, args.lifespan,
                                                   args.provider, args.release, args.release_version, "master", args.hardware, args.lifespan,
                                                   args.environment, args.hd, args.net, args.port)
        elif args.subcmd == 'update':
            if args.id is None:
                show_error("Parameter 'id' is required.")
                maccli.command_cli.instance_update_help()
            else:
                maccli.command_cli.instance_update(args.id, args.configuration, args.bootstrap)

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
            maccli.command_cli.instance_log(args.id, args.follow)

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

    elif args.cmd == "infrastructure" or args.cmd == 'infra':
        if args.subcmd == 'list':
            maccli.command_cli.infrastructure_list()
        elif args.subcmd == 'macfile':
            maccli.command_cli.process_macfile(args.file[0], args.resume, args.param, args.quiet, args.on_failure)
        elif args.subcmd == 'items':
            maccli.command_cli.infrastructure_search(args.name, args.version)
        elif args.subcmd == 'destroy':
            maccli.command_cli.infrastructure_destroy(args.name, args.version)
        elif args.subcmd == 'update':
            maccli.command_cli.infrastructure_update(args.name, args.version, args.configuration)
        elif args.subcmd == 'lifespan':
            maccli.command_cli.infrastructure_lifespan(args.amount, args.name, args.version)
        elif args.subcmd == 'sshkey':
            maccli.command_cli.infrastructure_ssh_keys(args.name, args.version, args.known_host)

    elif args.cmd == "provider":
        if args.subcmd == 'credential':
            maccli.command_cli.credentials(args.provider, args.clientid, args.key, args.force_file)

    elif args.cmd == "resource":
        if args.subcmd == 'get_stdout':
            maccli.command_cli.resouce_get_stdout(args.infrastructure_name, args.infrastructure_version, args.resource_name, args.key)


def parse_args(self, args):
    # factored out for testability
    return self.parser.parse_args(args)


def main():
    parser = initialize_parser()
    argv = patch_help_option(sys.argv)
    #if argv == ['-i']:  # interactive session
    #    maccli.interactive.start()
    #else:  # Normal session
    args = parser.parse_args(argv)
    dispatch_cmds(args)


if __name__ == "__main__":
    main()