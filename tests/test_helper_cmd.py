import unittest

from mock_data import *
import maccli.helper.cmd

#
#   For this unit testing, I needed to evaluate how popen behaves,
#   therefore subprocess.Popen is not mocked up. Ideas are welcomed!
#


class CmdTestCase(unittest.TestCase):

    def test_working_command(self):
        rc, stdout, stderr = maccli.helper.cmd.run("true")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

    def test_not_found(self):
        rc, stdout, stderr = maccli.helper.cmd.run("command_not_found")
        self.assertEqual(rc, 127)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, '/bin/bash: command_not_found: command not found\n')

    def test_stdout(self):
        rc, stdout, stderr = maccli.helper.cmd.run("echo hello")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout, "hello\n")
        self.assertEqual(stderr, "")

    def test_stderr(self):
        rc, stdout, stderr = maccli.helper.cmd.run("date invalid_date")
        self.assertEqual(rc, 1)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, 'date: invalid date \xe2\x80\x98invalid_date\xe2\x80\x99\n')

    def test_environment_variables(self):
        rc, stdout, stderr = maccli.helper.cmd.run('MY_ENV=1 env | grep MY_ENV')
        self.assertEqual(rc, 0)
        self.assertEqual(stdout, 'MY_ENV=1\n')
        self.assertEqual(stderr, "")

    def test_single_quotes(self):
        rc, stdout, stderr = maccli.helper.cmd.run("ls '*'")
        self.assertEqual(rc, 2)
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, 'ls: cannot access *: No such file or directory\n')

    def test_double_quotes(self):
        rc, stdout, stderr = maccli.helper.cmd.run('ls "*"')
        self.assertEqual(rc, 2)
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, 'ls: cannot access *: No such file or directory\n')
