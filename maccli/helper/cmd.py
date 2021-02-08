import os
import subprocess
from rfc3987 import parse

from maccli.helper.exception import MacApiError, MacAuthError, BashException
import maccli


def update_pwd(path_or_url):
    try:
        parse(path_or_url, rule='URI')
    except ValueError as e:
        maccli.pwd = os.path.dirname(os.path.realpath(path_or_url))


def run(command):
    cmd_parts = ["/bin/bash", "-c", command]
    maccli.logger.debug("Running bash: %s " % command)
    try:
        process = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=maccli.pwd)
    except Exception as e:
        raise BashException("%s: %s" % (command, e))

    process.wait()
    rc = process.returncode
    stdout, stderr = process.communicate()
    maccli.logger.debug("STDOUT: %s" % stdout)
    maccli.logger.debug("STDERR: %s" % stderr)
    return rc, stdout.decode('utf-8', 'ignore'), stderr.decode('utf-8', 'ignore')
