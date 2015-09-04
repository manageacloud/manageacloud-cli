import maccli
from maccli.helper.exception import BashException, MacResourceException, InstanceDoesNotExistException
import maccli.helper.macfile
import maccli.helper.cmd

__author__ = 'tk421'

#
#   Process resource type
#


def run_raw_command(infrastructure_key, command_raw, log_type, key, instances, roles, infrastructures, actions, processed_resources):
    """ Executes a command that will create a resource or run an action """

    maccli.logger.debug("%s %s command_raw: %s " % (log_type, key, command_raw))
    command_clean = command_raw

    # output if the resource has been processed
    is_resource_processed = True
    resource_processed = {}
    is_parsed = True
    if maccli.helper.macfile.has_dependencies(command_raw, roles, infrastructures, actions):
        maccli.logger.debug("Running %s %s with dependency" % (log_type, key))
        try:
            command_clean, is_parsed = maccli.helper.macfile.parse_envs(command_raw, instances, roles, infrastructures, actions, processed_resources)
        except BashException as e:
            raise MacResourceException("Error: %s\nCommand: %s", e[0], e[1])

        except InstanceDoesNotExistException as e:
            raise MacResourceException("Instance %s  does not exist " % e, "Instance %s  does not exist " % e)
    else:
        maccli.logger.debug("Running %s %s with no dependency" % (log_type, key))

    if is_parsed:
        maccli.logger.debug("%s %s command_clean: %s " % (log_type, key, command_raw))
        rc, stdout, stderr = maccli.helper.cmd.run(command_clean)

        if rc == 0:
            resource_processed = {'stderr': stderr, 'stdout': stdout, 'rc': rc, 'cmd': command_clean}
        else:
            raise MacResourceException("Error while executing resource %s " % infrastructure_key, {'stderr': stderr, 'stdout': stdout, 'rc': rc, 'cmd': command_clean})
    else:
        is_resource_processed = False

    return resource_processed, is_resource_processed