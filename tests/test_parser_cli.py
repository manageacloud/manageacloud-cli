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

    def test_validate_hd(self):
        self.assertEqual(maccli.parser_cli.validate_hd("/dev/sda1:100"), {'/dev/sda1':'100'})
        self.assertEqual(maccli.parser_cli.validate_hd("/dev/sda1:50"), {'/dev/sda1':'50'})
        self.assertEqual(maccli.parser_cli.validate_hd("attachment:50:ssd"), {'attachment':'50:ssd'})
        self.assertEqual(maccli.parser_cli.validate_hd("/dev/ok:100"), {'/dev/ok':'100'})
        self.assertEqual(maccli.parser_cli.validate_hd("/dev/sda1:100:ok"), {'/dev/sda1':'100:ok'})
        self.assertEqual(maccli.parser_cli.validate_hd("/dev/sda1:100:ok:1000"), {'/dev/sda1':'100:ok:1000'})
        #self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "/dev/not/ok:100")
        #self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "/not/ok:100")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "/dev/ok:wtf")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "/dev/ok")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "100")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_hd, "/dev/sda1:100:not-ok")

    def test_validate_port(self):
        self.assertEqual(maccli.parser_cli.validate_port("22"), [22])
        self.assertEqual(maccli.parser_cli.validate_port("22,8080"), [22,8080])
        self.assertEqual(maccli.parser_cli.validate_port("1,22,8080,65535"), [1,22,8080,65535])
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_port, "0,22,8080,65535")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_port, "22,8080,65536")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_port, "22,sssss8080")
        self.assertRaises(ArgumentTypeError, maccli.parser_cli.validate_port, "sssss8080")
