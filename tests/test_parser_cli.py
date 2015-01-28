import unittest

import mock
from argparse import ArgumentTypeError

from mock_data import *
import maccli.parser_cli


class ParserCliTestCase(unittest.TestCase):

    def test_validate_environment(self):
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_environment, "invalid")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_environment, "invalid = spaces")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_environment, "BENCH_CREATION=")
        self.assertEqual(maccli.parser_cli.validate_environment("UNO=dos"), {'UNO':'dos'})
        self.assertEqual(maccli.parser_cli.validate_environment("uno=dos"), {'uno':'dos'})
        self.assertEqual(maccli.parser_cli.validate_environment("A_VALUE=dos2"), {'A_VALUE':'dos2'})
        self.assertEqual(maccli.parser_cli.validate_environment("a_value=dos2"), {'a_value':'dos2'})
        self.assertEqual(maccli.parser_cli.validate_environment("a_value=dos2=3"), {'a_value':'dos2=3'})
        self.assertEqual(maccli.parser_cli.validate_environment("BENCH_CREATION=-i -s 70"), {'BENCH_CREATION':'-i -s 70'})
