#
#   Interactive session is a preview feature.
#   Please use with care.
#

from __future__ import unicode_literals
import shlex
from prompt_toolkit.styles import DefaultStyle
from maccli.helper.exception import InternalError
from maccli.view.view_generic import show

__author__ = 'tk421'

from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.layout.lexers import SimpleLexer
from prompt_toolkit.contrib.regular_languages.compiler import compile
import maccli.mac_cli
import maccli

from pygments.token import Token


op_mac = ['mac']
op_main = ['login', 'instance', 'configuration', 'infrastructure']
op_instance = ['list', 'create', 'update', 'destroy', 'ssh', 'facts', 'log', 'lifespan']
op_configuration = ['list', 'search']
op_infrastructure = ['macfile', 'list', 'items', 'destroy', 'update', 'lifespan', 'sshkey']


def create_grammar():
    return compile("""
        ((?P<op_mac>mac)    \s*  (?P<op_main>login)   \s+) |
        ((?P<op_mac>mac)    \s*  (?P<op_main>instance)   \s+   (?P<op_instance>[list|create|update|destroy|ssh|facts|log|lifespan]+)    \s+    (?P<op_parameter>("[^"]*"|[^"]+)(\s+|$))    \s+) |
        ((?P<op_mac>mac)    \s*  (?P<op_main>configuration)   \s+   (?P<op_configuration>[list|search]+)    \s+    (?P<op_parameter>("[^"]*"|[^"]+)(\s+|$))    \s+) |
        ((?P<op_mac>mac)    \s*  (?P<op_main>infrastructure)   \s+   (?P<op_infrastructure>[macfile|list|items|destroy|update|lifespan|sshkey]+)    \s+    (?P<op_parameter>("[^"]*"|[^"]+)(\s+|$))    \s+)
    """)


class MacStyle(DefaultStyle):
    styles = {}
    styles.update(DefaultStyle.styles)
    styles.update({
        Token.Operator: '#33aa33 bold',
        Token.Number: '#aa3333 bold',
        Token.Text: '#7A8DF5 bold',

        Token.TrailingInput: 'bg:#662222 #ffffff',
        })


def start():

    g = create_grammar()

    lexer = GrammarLexer(g, lexers={
        'op_mac': SimpleLexer(Token.Operator),
        'op_main': SimpleLexer(Token.Operator),
        'op_instance': SimpleLexer(Token.Operator),
        'op_configuration': SimpleLexer(Token.Operator),
        'op_infrastructure': SimpleLexer(Token.Operator),
        'op_parameter': SimpleLexer(Token.Text),
        })

    completer = GrammarCompleter(g, {
        'op_main': WordCompleter(op_main),
        'op_instance': WordCompleter(op_instance),
        'op_configuration': WordCompleter(op_configuration),
        'op_infrastructure': WordCompleter(op_infrastructure),
        })

    history = InMemoryHistory()

    parser = maccli.mac_cli.initialize_parser()

    show("Start typing 'mac', CTRL+C to exit")
    user_aborted = False
    program_running = True
    while program_running:
        try:
            text = prompt('> ', lexer=lexer, completer=completer, style=MacStyle, history=history, auto_suggest=AutoSuggestFromHistory())
            argv_raw = shlex.split(text)
            argv = maccli.mac_cli.patch_help_option(argv_raw)
            args = parser.parse_args(argv)
            maccli.mac_cli.dispatch_cmds(args)
            user_aborted = False
        except InternalError as e:
            maccli.logger.debug("Code raised Internal Error", e)
            pass
        except EOFError as e:
            maccli.logger.debug("Code raised EOFError", e)
            pass
        except KeyboardInterrupt as e:
            maccli.logger.debug("Code raised KeyboardInterrupt", e)
            if user_aborted:
                program_running = False
            else:
                user_aborted = True
                show("Press CTRL+C again to exit")
            pass




