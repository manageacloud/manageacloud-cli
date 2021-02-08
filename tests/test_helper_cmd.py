import os
import unittest

from tests.mock_data import *
import maccli.helper.cmd

#
#   For this unit testing, I needed to evaluate how popen behaves,
#   therefore subprocess.Popen is not mocked up. Ideas are welcomed!
#


class CmdTestCase(unittest.TestCase):

    def setUp(self):
        maccli.pwd = os.getcwd()

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
        self.assertEqual(stderr, 'date: invalid date ‘invalid_date’\n')

    def test_environment_variables(self):
        rc, stdout, stderr = maccli.helper.cmd.run('MY_ENV=1 env | grep MY_ENV')
        self.assertEqual(rc, 0)
        self.assertEqual(stdout, 'MY_ENV=1\n')
        self.assertEqual(stderr, "")

    def test_single_quotes(self):
        rc, stdout, stderr = maccli.helper.cmd.run("ls '*'")
        self.assertEqual(rc, 2)
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, 'ls: cannot access \'*\': No such file or directory\n')

    def test_double_quotes(self):
        rc, stdout, stderr = maccli.helper.cmd.run('ls "*"')
        self.assertEqual(rc, 2)
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, 'ls: cannot access \'*\': No such file or directory\n')

    def test_absolute_path(self):
        path = '/this/is/absolute'
        myfile = path + '/path'
        maccli.helper.cmd.update_pwd(myfile)
        self.assertEqual(maccli.pwd, path)

    def test_relative_path(self):
        path = 'is/relative'
        myfile = path + '/path'
        maccli.helper.cmd.update_pwd(myfile)
        self.assertEqual(maccli.pwd, os.getcwd() + "/" + path)

    def test_url(self):
        old_pwd = maccli.pwd
        maccli.helper.cmd.update_pwd('https://manageacloud.com/my/path')
        self.assertEqual(maccli.pwd, old_pwd)
