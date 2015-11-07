import json
import re
import maccli
from maccli.helper.exception import BashException, MacResourceException, InstanceDoesNotExistException
import maccli.helper.macfile
import maccli.helper.cmd
import maccli.helper.metadata
import maccli.dao.api_resource

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
            infrastructure = infrastructures[infrastructure_key]
            command_clean, is_parsed = maccli.helper.macfile.parse_envs(command_raw, instances, roles, infrastructures, actions, processed_resources, infrastructure)
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


def create_resource(root, infrastructure_key, name, create_bash, rc, stderr, stdout, destroy_bash, infrastructure):
    """
        create a resource
    """
    metadata = maccli.helper.metadata.metadata_resource(root, infrastructure_key, name, infrastructure)
    return maccli.dao.api_resource.create(infrastructure_key, create_bash, rc, stderr, stdout, destroy_bash, metadata)


def update_resource(resource, destroy_bash, rc, stderr, stdout):
    """
        Updates a resource and adds the output for destroying it
    """
    resource['destroy'] = {
        'cmd': destroy_bash,
        'rc': rc,
        'stderr': stderr,
        'stdout': stdout
    }
    return maccli.dao.api_resource.update(resource)


def destroy_resource(resource):
    """
        Destroy the resource
    """
    return maccli.dao.api_resource.delete(resource)


def get_resource_value(inf_name, inf_version, resource_name, key):
    """
        Gets the resource
    """
    resource = maccli.dao.api_resource.get(inf_name, inf_version, resource_name)

    stdout_raw = resource['create']['stdout']
    stdout = ""

    if key is None:
        stdout = stdout_raw
    elif key[:4] == "json":
        stdout_json = json.loads(stdout_raw.strip())
        if key == "json":
            stdout = json.dumps(stdout_json, indent=4)
        elif key[:5] == "json.":
            raw_keys = key[5:].split(".")
            value = stdout_json
            for key in raw_keys:
                if key.isdigit():
                    value = value[int(key)]
                else:
                    value = value[key]

            if isinstance(value, basestring):
                stdout = value
            else:
                stdout = json.dumps(value, indent=4)

    elif key[:4] == "text":
        # accepted values
        # text
        # text.regex(my_regex)
        # text.regex(my_regex)[1] # witht he position that we are going to extract
        if key == "text":
            stdout = stdout_raw
        elif key[:11] == "text.regex(":
            # format text.regex(my_regex)
            regex_extract = re.compile("text.regex\((.*)\)", re.IGNORECASE)

            # match text
            regex_pattern = regex_extract.findall(key)[0]
            maccli.logger.debug("Searching %s at %s " % (regex_pattern, stdout_raw.strip()))
            regex = re.compile(regex_pattern, re.IGNORECASE)
            matches = regex.findall(stdout_raw.strip())

            # get the proper position
            position_extract_regex = re.compile("text.regex\(.*\)\[([0-9]+)\]", re.IGNORECASE)
            positions = position_extract_regex.findall(key)
            if len(matches) and len(positions):
                stdout = matches[int(positions[0])]
            else:
                stdout = matches

    return stdout