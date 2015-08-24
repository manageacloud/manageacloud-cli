import json
from maccli.helper.exception import InstanceNotReadyException, InstanceDoesNotExistException, BashException
import maccli.service.instance
__author__ = 'tk421'
import re
import maccli
import maccli.helper.cmd


def has_dependencies(text, roles, infrastructures, actions):
    """ check of there are dependencies in the text
        a dependency is somthing with the format:
         - role.[role_name].[action]
         - infrastructure.[infrastructure name].[action]

        returns true of false

    """
    # TODO add validation for resources
    # TODO add validation for cases where name is incorrect. e.g infrastructure.image_base.get_id instead infrastructure.image_base_inf.get_id
    has_deps = False
    matches = get_dependencies(text)
    if matches:
        for match in matches:
            type_name = match[0]
            name = match[1]
            action = match[2]
            maccli.logger.debug("Match found: type '%s' name '%s' action '%s' " % (type_name, name, action))
            if type_name == "role" and name in roles or type_name == "infrastructure" and name in infrastructures:
                if action in actions:
                    has_deps = True
                elif name in infrastructures and action in infrastructures[name]:
                    has_deps = True
                else:
                    maccli.logger.warn("%s.%s.%s has been found but %s does not match with an action"
                                       % (type_name, name, action, action))
            elif type_name == "resource":  # TODO add more validation
                has_deps = True

            elif type_name == "action":
                has_deps = True

            else:
                maccli.logger.warn("'%s.%s.%s' has been found but we do not how to process '%s' "
                                   % (type_name, name, action, type_name))
    maccli.logger.debug("has_dependencies? %s" % has_deps)
    return has_deps


def is_role_dependencies_ready(infrastructure, processed_instances, infrastructure_key):
    """ Return if the role dependencies are ready """
    ready = True # we just return a boolean we are not ready
    if 'ready' in infrastructure:  # check if infrastructure has dependencies
        instances_ready = infrastructure['ready']  # role.app
        maccli.logger.debug("Infrastructure %s infrastructure_key requires %s ready before proceeding" % (infrastructure_key, instances_ready))
        instance_type, role_name = instances_ready.split(".")

        for instance in processed_instances:
            instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
            instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']
            if instance_role_name == role_name or instance_infrastructure_name == role_name:
                if not ("Error" in instance['status'] or instance['status'].startswith("Ready")):
                    maccli.logger.info("%s is not ready yet, waiting ...", instance['id'])
                    ready = False
                    break  # exit from loop to avoid processing other resources
    return ready


def get_dependencies(text):
    """ check of there are dependencies in the text
        a dependency is somthing with the format:
         - role.[role_name].[action]
         - infrastructure.[infrastructure name].[action]

        returns true of false
    """
    a = re.compile("(role|infrastructure|resource|action)\.([a-zA-Z0-9_\-\.]*?)\.([a-zA-Z0-9_\-\.]*)($|\s|\"|')", re.IGNORECASE)
    matches = a.findall(text)

    maccli.logger.debug("Searching for dependencies at %s" % text)
    return matches


def get_action_ssh(name, actions):
    toreturn = ""
    for action_key in actions:
        if action_key == name:
            toreturn = actions[action_key]['ssh']
            break
    return toreturn


def get_action_bash(name, actions):
    toreturn = ""
    for action_key in actions:
        if action_key == name:
            toreturn = actions[action_key]['bash']
            break
    return toreturn


def parse_envs(text, instances, roles, infrastructures, actions, processed_resources):
    """ replace the dependencies between roles using actions
        a dependency is somthing with the format:
         - role.[role_name].[action]
         - infrastructure.[infrastructure name].[action]

        returns true of false
    """
    all_processed = True
    matches = get_dependencies(text)
    if matches:
        for match in matches:
            type_name = match[0]
            name = match[1]
            action = match[2]
            maccli.logger.debug("Match found: type '%s' name '%s' action '%s' " % (type_name, name, action))

            match_processed = False
            if name in infrastructures and action in infrastructures[name]:
                #  search in infrastructures
                #  the substitution is an infrastructure
                value = infrastructures[name][action]
                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                match_processed = True

            elif any(name in d for d in processed_resources):
                # search in resources
                for processed_resource in processed_resources:
                    if name in processed_resource:
                        value_raw = processed_resource[name]['stdout']
                        text_format, text_id_raw = action.split(".", 1)

                        if text_format == "json":
                            try:
                                texts = text_id_raw.split(".")
                                value_json = json.loads(value_raw.strip())
                                value = value_json
                                for text_part in texts:
                                    if text_part.isdigit():
                                        value = value[int(text_part)]
                                    else:
                                        value = value[text_part]

                                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                                match_processed = True
                            except KeyError:
                                match_processed = False

                        else:
                            raise NotImplementedError

            elif type_name == "action" and name in actions:
                # Executes the action, it is currently adhoc only for 'json'

                bash_command_raw = get_action_bash(name, actions)

                # bash command might have parameters to be replaced
                if has_dependencies(bash_command_raw, roles, infrastructures, actions):
                    bash_command, processed = parse_envs(bash_command_raw, instances, roles, infrastructures, actions, processed_resources)
                else:
                    bash_command = bash_command_raw

                rc = None
                stdout = None
                try:
                    rc, stdout, stderr = maccli.helper.cmd.run(bash_command)
                except Exception as e:
                    maccli.logger.warn("Error executing %s: %s" % (bash_command, e))

                if rc is not None:
                    if rc == 0:
                        parts = action.split(".")
                        action_type = parts.pop(0)
                        value_json = json.loads(stdout.strip())
                        value = value_json

                        # get value from json structure
                        if action_type == "json":
                            for part in parts:
                                if part.isdigit():
                                    value = value[int(part)]
                                else:
                                    value = value[part]

                        else:
                            raise NotImplementedError

                        text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                        match_processed = True
                    else:
                        maccli.logger.warn("Error executing bash action %s: %s" % (bash_command, stderr))
                        #raise BashException("Error executing bash action %s: %s" % (bash_command, stderr), stderr)
                        match_processed = False

            elif action in actions:
                # search in actions
                outputs = []

                # execute the action in an instance
                for instance in instances:
                    if type_name == "role" and name in roles:
                        matching_name = instance['metadata']['infrastructure']['macfile_role_name']
                    elif type_name == "infrastructure" and name in infrastructures:
                        matching_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']
                    else:
                        #  this method ignores the replacement
                        matching_name = ""

                    if matching_name and matching_name == name:
                        ssh_command = get_action_ssh(action, actions)
                        rc = None
                        try:
                            rc, ssh_raw, stderror = maccli.service.instance.ssh_command_instance(instance['id'], ssh_command)
                        except InstanceNotReadyException:
                            rc = -1
                        finally:
                            if rc is not None:
                                if rc == 0:
                                    outputs.append(ssh_raw)
                                    match_processed = True
                                else:
                                    maccli.logger.warn("Error executing ssh action %s: %s" % (bash_command, stderr))
                                    match_processed = False
                                    break

                text = text.replace("%s.%s.%s" % (type_name, name, action), " ".join(outputs))

            all_processed = all_processed and match_processed

            if not all_processed:
                break

    return text, all_processed