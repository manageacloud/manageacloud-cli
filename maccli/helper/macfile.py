import json
from maccli.helper.exception import InstanceNotReadyException, InstanceDoesNotExistException, BashException, \
    MacParameterNotFound
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

            elif type_name == "infrastructure" and name == "param":
                # TODO check if the param actually exists for every infrastructure that calls that resource
                has_deps = True

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
         - resource.something.text.regex(myregex)
        returns true of false
    """
    try:
        a = re.compile("(role|infrastructure|resource|action)\.([a-zA-Z0-9_\-\.]*?)\.([a-zA-Z0-9_\-\.]*|text\.regex\((.+)\))($|\s|\"|')", re.IGNORECASE)
        matches = a.findall(text)
        maccli.logger.debug("Searching for dependencies at %s" % text)
    except TypeError:  # not an string, no dependencies
        maccli.logger.debug("'%s' is not an string", text)
        matches = []

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


def dict_has_dependencies(dict, roles, infrastructures, actions):
    """
    Check if dictionary's values has dependencies

    :param dict:
    :param roles:
    :param infrastructures:
    :param actions:
    :return:
    """
    toreturn = False
    for key in dict.keys():
        text_raw = dict[key]
        if has_dependencies(text_raw, roles, infrastructures, actions):
            toreturn = True
            break
    return toreturn


def parse_envs_dict(dict, instances, roles, infrastructures, actions, processed_resources):
    """
    Loops over a dictionary to find values that must be processed.

    :param dict: dictionary input
    :param instances:
    :param roles:
    :param infrastructures:
    :param actions:
    :param processed_resources:
    :return: dictionary with values processed, and if all values could be processed
    """
    total_processed = True
    for key in dict.keys():
        text_raw = dict[key]
        if isinstance(text_raw, basestring):
            text, processed = parse_envs(text_raw, instances, roles, infrastructures, actions, processed_resources)
            total_processed = total_processed and processed
            if processed:
                dict[key] = text

    return dict, total_processed


def parse_envs(text, instances, roles, infrastructures, actions, processed_resources, infrastructure=None):
    """
        replace the dependencies

    :param text: text that contains dependencies
    :param instances: instances from the context
    :param roles: roles available in the context
    :param infrastructures: all the infrastructures available in the context
    :param actions: all the actions available in the context
    :param processed_resources: all the processed resources, including output of commands
    :param infrastructure: the infrastructure that we are executing. Not available for all the contexts.
    :return:
    """

    all_processed = True

    # let's get all the dependencies of variables that we have to substitute
    matches = get_dependencies(text)

    # loop every variable
    if matches:
        for match in matches:
            type_name = match[0]
            name = match[1]
            action = match[2]
            maccli.logger.debug("Match found: type '%s' name '%s' action '%s' " % (type_name, name, action))

            # now we process the variables depending on the strategy to solve

            # We check if the matches are processed. If it is not possible to process in this iteration, we might
            # not have all the required information yet.
            match_processed = False

            # parse values from "infrastructures" section in the macfile
            if name in infrastructures and action in infrastructures[name]:
                #  search in infrastructures
                #  the substitution is an infrastructure
                value = infrastructures[name][action]
                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                match_processed = True

            # parse values from "infrastructures.params" section in the macfile. This is a bit different because keys are
            # arbitrary
            elif type_name == "infrastructure" and name == "param":

                if not infrastructure:
                    maccli.logger.warn("Infrastructure context not provided to substitute %s.%s.%s" % (type_name, name, action))

                elif 'params' not in infrastructure:
                    maccli.logger.warn("Infrastructure context does not have params %s" % infrastructure)

                elif action in infrastructure['params']:

                    # the params value could require a substitution
                    value_raw = infrastructure['params'][action]
                    if has_dependencies(value_raw, roles, infrastructures, actions):
                        value, processed = parse_envs(value_raw, instances, roles, infrastructures, actions, processed_resources, infrastructure)
                    else:
                        processed = True
                        value = value_raw

                    if processed:
                        text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                        match_processed = True

            # match values that are processed resources
            elif any(name in d for d in processed_resources) and not (action in actions):
                # search in resources
                for processed_resource in processed_resources:
                    if name in processed_resource:
                        value_raw = processed_resource[name]['stdout']

                        try:
                            text_format, text_id_raw = action.split(".", 1)
                        except ValueError:
                            raise MacParameterNotFound("The value %s in the parameter %s.%s does not have the proper format." % (action, type_name, name))

                        # output format is json
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
                                if not(value_raw == '' or value_raw is None):
                                    original_task = "%s.%s.%s" % (type_name, name, action)
                                    maccli.logger.warn("We cannot find '%s' at '%s'" % (original_task, name))
                                    maccli.logger.debug("Original value: %s" % value_raw)
                                match_processed = False

                        # output format is text, and it will be processed with a regular expression
                        elif text_format == "text":
                            try:
                                regex_pattern = match[3]
                                maccli.logger.debug("Regex marching: %s at value %s " % (regex_pattern, value_raw))
                                regex = re.compile(regex_pattern, re.IGNORECASE)
                                matches = regex.findall(value_raw.strip())
                                maccli.logger.debug("Matches %s" % matches)
                                value = matches[0]
                                text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                                match_processed = True
                            except Exception as e:
                                maccli.logger.debug("Error matching regex %s at value %s because of %s" % (match[3], value_raw, e))
                                maccli.logger.warn("Error matching regex %s at value %s" % (match[3], value_raw))
                                match_processed = False

                        else:
                            raise NotImplementedError

            # process if it is an action, but it is bash and will be executed from
            # the machine that is running the macfile
            elif type_name == "action" and name in actions:
                # Executes the action, it is currently adhoc only for 'json'

                bash_command_raw = get_action_bash(name, actions)

                # bash command might have parameters to be replaced
                if has_dependencies(bash_command_raw, roles, infrastructures, actions):
                    bash_command, processed = parse_envs(bash_command_raw, instances, roles, infrastructures, actions, processed_resources, infrastructure)
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

            # action is related with an instance, and it will be executed via SSH
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
                        stderr = None
                        try:
                            rc, ssh_raw, stderr = maccli.service.instance.ssh_command_instance(instance['id'], ssh_command)
                        except InstanceNotReadyException:
                            rc = -1
                        finally:
                            if rc is not None:
                                if rc == 0:
                                    outputs.append(ssh_raw)
                                    match_processed = True
                                else:
                                    if stderr is not None:
                                        maccli.logger.warn("Error executing ssh action %s: %s" % (ssh_command, stderr))
                                    match_processed = False
                                    break

                text = text.replace("%s.%s.%s" % (type_name, name, action), " ".join(outputs))
            else:
                # This parameter cannot be executed
                if not name in infrastructures:
                    raise MacParameterNotFound("The parameter %s.%s has not been found while processing %s " % (type_name, name, text))

            all_processed = all_processed and match_processed

            if not all_processed:
                break

    return text, all_processed


def parse_envs_destroy(resource_to_destroy, instances, resources):
    """ parse envs for the destroy event
            - resource.[infrastructure_name].json.jsonValue
            - infrastructure.param.paramname
    """
    text = resource_to_destroy['cmdDestroy']
    matches = get_dependencies(text)
    if matches:
        for match in matches:
            type_name = match[0]
            name = match[1]
            action = match[2]
            maccli.logger.debug("Match found: type '%s' name '%s' action '%s' " % (type_name, name, action))

            if type_name == "resource":
                for resource in resources:
                    if name == resource['metadata']['infrastructure']['macfile_infrastructure_name']:
                        parts = action.split(".")
                        action_type = parts.pop(0)
                        value_json = json.loads(resource['create']['stdout'].strip())
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

            elif type_name == "infrastructure" and name == "param":

                if 'macfile_infrastructure_params' in resource_to_destroy['metadata']['infrastructure']:
                    if action in resource_to_destroy['metadata']['infrastructure']['macfile_infrastructure_params']:
                        value = resource_to_destroy['metadata']['infrastructure']['macfile_infrastructure_params'][action]
                        text = text.replace("%s.%s.%s" % (type_name, name, action), value)
                    else:
                        maccli.logger.warn("Param %s not found when processing %s.%s.%s to destroy resource" % (action, type_name, name, action))
                else:
                    maccli.logger.warn("Warning while destroying resource! Params are not available and are required for %s.%s.%s" % (type_name, name, action))
    return text
