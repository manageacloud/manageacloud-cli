import subprocess

from maccli.helper.exception import MacApiError, MacAuthError
import maccli


def run(command):
    cmd_parts = command.strip().split(" ")
    maccli.logger.debug("Running bash: %s " % command)
    process = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    rc = process.returncode
    stdout, stderr = process.communicate()
    maccli.logger.debug("STDOUT: %s" % stdout)
    maccli.logger.debug("STDERR: %s" % stderr)
    return rc, stdout, stderr
