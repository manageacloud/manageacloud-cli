import json
from maccli.helper.exception import InstanceNotReadyException, InstanceDoesNotExistException
import maccli.service.instance
__author__ = 'tk421'
import re
import maccli


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
            else:
                maccli.logger.warn("%s.%s.%s has been found but %s does not match with a %s"
                                   % (type_name, name, action, name, type_name))
    maccli.logger.debug("has_dependencies? %s" % has_deps)
    return has_deps


def get_dependencies(text):
    """ check of there are dependencies in the text
        a dependency is somthing with the format:
         - role.[role_name].[action]
         - infrastructure.[infrastructure name].[action]

        returns true of false
    """
    a = re.compile("(role|infrastructure|resource)\.([a-zA-Z0-9_\-\.]*?)\.([a-zA-Z0-9_\-\.]*)($|\s)", re.IGNORECASE)
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
                #  the substitution is an infrastructure
                value = infrastructures[name][action]
                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                match_processed = True

            elif any(name in d for d in processed_resources):
                for processed_resource in processed_resources:
                    if name in processed_resource:
                        value_raw = processed_resource[name]['stdout']
                        text_format, text_id = action.split(".")

                        if text_format == "json":
                            try:
                                value_json = json.loads(value_raw.strip())
                                value = value_json[text_id]
                                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                                match_processed = True
                            except KeyError:
                                match_processed = False

                        else:
                            raise NotImplementedError

            elif action in actions:
                #  substitution is an action
                outputs = []
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
                                    match_processed = False
                                    break

                text = text.replace("%s.%s.%s" % (type_name, name, action), " ".join(outputs))

            all_processed = all_processed and match_processed

            if not all_processed:
                break

    return text, all_processed