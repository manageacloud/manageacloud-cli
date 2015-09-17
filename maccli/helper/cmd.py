import subprocess

from maccli.helper.exception import MacApiError, MacAuthError, BashException
import maccli


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
    return rc, stdout, stderr
