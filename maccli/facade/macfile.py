from __future__ import print_function
import time
import maccli

import pprint
from maccli.config import MACFILE_ON_FAILURE_DESTROY_OTHERS, MACFILE_ON_FAILURE_DESTROY_ALL
import maccli.service.instance
import maccli.view.view_generic
import maccli.view.view_instance
import maccli.view.view_infrastructure
import maccli.helper.macfile
import maccli.helper.cmd
from maccli.helper.network import is_ip_private, is_local
from maccli.helper.exception import MacParseEnvException, FactError, MacApiError, MacResourceException, \
    InstanceNotReadyException, InstanceDoesNotExistException

pp = pprint.PrettyPrinter(indent=4)


def _get_private_ip_from_fatcs(facts):
    if facts is not None and 'interfaces' in facts:
        interfaces = facts['interfaces'].split(",")
        priv_ip = ""
        fallback_ip = ""
        for interface_key in interfaces:
            ip_raw = facts["ipaddress_%s" % interface_key]
            if is_ip_private(ip_raw) and not is_local(ip_raw):
                priv_ip = ip_raw
                break
            elif fallback_ip == "" and not is_local(ip_raw):
                fallback_ip = ip_raw

        if priv_ip != "":
            ip = priv_ip
        else:
            ip = fallback_ip
    else:
        raise FactError("Interfaces not available")

    return ip


def _get_environment(role, infrastructure):
    environment = None
    try:
        if 'environment' in infrastructure.keys():
            environment = infrastructure["environment"]

        if 'environment' in role.keys():
            if environment is not None:
                environment = environment + role["environment"]
            else:
                environment = role["environment"]

    except KeyError:
        pass

    return environment


def create_tier(role, infrastructure, metadata, quiet):
    """
        Creates tje instances that represents a role in a given infrastructure

    :param role:
    :param infrastructure:
    :return:
    """

    lifespan = None
    try:
        lifespan = infrastructure['lifespan']
    except KeyError:
        pass

    hardware = ""
    try:
        hardware = infrastructure["hardware"]
    except KeyError:
        pass

    environment = _get_environment(role, infrastructure)

    hd = None
    try:
        hd = role["hd"]
    except KeyError:
        pass

    port = None
    try:
        port = infrastructure["port"]
    except KeyError:
        pass

    deployment = None
    try:
        deployment = infrastructure["deployment"]
    except KeyError:
        pass

    release = None
    try:
        release = infrastructure["release"]
    except KeyError:
        pass

    branch = None
    try:
        branch = infrastructure["branch"]
    except KeyError:
        pass

    provider = None
    try:
        provider = infrastructure["provider"]
    except KeyError:
        pass

    instances = []
    amount = 1
    if 'amount' in infrastructure:
        amount = infrastructure['amount']

    for x in range(0, amount):
        instance = maccli.service.instance.create_instance(role["configuration"], deployment,
                                                           infrastructure["location"], infrastructure["name"],
                                                           provider, release, branch, hardware, lifespan,
                                                           environment, hd, port, metadata, False)
        instances.append(instance)
        print("Creating instance '%s'" % (instance['id']))

    if not quiet:
        print()
        print()
    return instances


def parse_instance_envs(env_raws, instances):
    """
        Replaces the values in the environment variables for values
        that exist in this infrastructure

        Supported:

         - role.PUBLIC_IP -> adds the public ip
         - role.PRIVATE_IP -> adds the first private ip retrieved by facts
         - role.FACT.FACTNAME -> replace fact by any other fact

    :param role:
    :param roles_created:
    :return:
    """

    envs_clean = {}
    all_processed = True
    for env in env_raws:
        key = env.keys()[0]
        val = env[key]
        if isinstance(val, (int, long)):
            val = str(val)

        if isinstance(val, basestring):
            if val.endswith(".PUBLIC_IP"):
                """
                    We substitute the value by the given role
                    Format existing_role.PROPERTY
                """
                role_name, property = val.split(".", 1)
                try:
                    ips = []
                    for instance in instances:
                        instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
                        instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']

                        ip = instance['ipv4']
                        if ip and (instance_role_name == role_name or instance_infrastructure_name == role_name):
                            ips.append(ip)

                    if len(ips) > 0:
                        envs_clean[key] = ips
                    else:
                        all_processed = False
                except KeyError:
                    raise MacParseEnvException("Error while parsing env PUBLIC_IP", key, val)

            elif val.endswith(".PRIVATE_IP"):
                role_name, property = val.split(".", 1)
                try:
                    ips = []
                    is_error = False
                    for instance in instances:
                        instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
                        instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']
                        if instance_role_name == role_name or instance_infrastructure_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(instance['id'])
                                ip = _get_private_ip_from_fatcs(instance_facts)
                                ips.append(ip)
                            except FactError:
                                is_error = True
                                pass
                            except MacApiError:
                                is_error = True
                                pass

                    if len(ips) > 0 and not is_error:
                        envs_clean[key] = ips
                    else:
                        all_processed = False

                except KeyError:
                    raise MacParseEnvException("Error while parsing env PRIVATE_IP", key, val)

            elif ".FACT." in val:
                role_name, fact, property = val.split(".", 2)

                try:
                    facts = []
                    is_error = False
                    for instance in instances:
                        instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
                        instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']

                        if instance_role_name == role_name or instance_infrastructure_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(instance['id'])
                                property_value = instance_facts[property.lower()]
                                facts.append(property_value)
                            except FactError:
                                is_error = True
                                pass
                            except MacApiError:
                                is_error = True
                                pass

                    if len(facts) > 0 and not is_error:
                        envs_clean[key] = facts
                    else:
                        all_processed = False

                except KeyError:
                    raise MacParseEnvException("Error while parsing env PRIVATE_IP", key, val)

            else:
                envs_clean[key] = val

    return envs_clean, all_processed


def apply_instance_infrastructure_changes(instances, infrastructure_name, version, quiet, infrastructures, infrastructure_resources_processed):
    """
    Make sure that all instances in a infrastructure are processed
    :param instances:
    :return:
    """
    configuration_pending = []
    other_instances = []
    for instance in instances:

        if instance['status'] == "Instance completed":
            infrastructure_key = instance['metadata']['infrastructure']['macfile_infrastructure_name']
            infrastructure = infrastructures[infrastructure_key]
            dependencies_ready = maccli.helper.macfile.is_role_dependencies_ready(infrastructure, instances, infrastructure_key)
            if dependencies_ready:
                configuration_pending.append(instance)
            else:
                maccli.logger.debug("[%s] instance discarded as 'ready' dependencies are not met" % instance['servername'])

        if instance['ipv4'] is not None:
            other_instances.append(instance)

    action = False
    for instance in configuration_pending:
        maccli.logger.debug("[%s] Checking instance " % instance['servername'])
        cookbook_tag = instance['metadata']['system']['role']['cookbook_tag']
        instance_id = instance['id']

        # if there are dynamic variables
        if 'environment_raw' in instance['metadata']['infrastructure']:
            environment_raws = instance['metadata']['infrastructure']['environment_raw']
            maccli.logger.debug("[%s] Environment raw: %s" % (instance['servername'], environment_raws))
            maccli.logger.debug("[%s] Instances: %s" % (instance['servername'], other_instances))
            environment_clean, processed = parse_instance_envs(environment_raws, other_instances)
            maccli.logger.debug("[%s] Environment clean: %s" % (instance['servername'], environment_clean))
            metadata_new = {'system': {'role': {'environment': environment_clean}}}
            maccli.logger.debug("[%s] Process %s" % (instance['servername'], processed))
            if processed:
                action = True
                maccli.service.instance.update_configuration(cookbook_tag, instance_id, metadata_new)
                processing_instances = maccli.service.instance.list_by_infrastructure(infrastructure_name, version)
                if quiet:
                    maccli.view.view_generic.show("Applying configuration to %s" % instance['servername'])
                else:
                    maccli.view.view_generic.clear()
                    maccli.view.view_instance.show_instances(processing_instances)
                    maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)

        # there are not dynamic variables, it can start straight away
        else:
            action = True
            maccli.logger.debug("[%s] Processing ")
            maccli.service.instance.update_configuration(cookbook_tag, instance_id)
            processing_instances = maccli.service.instance.list_by_infrastructure(infrastructure_name, version)
            if quiet:
                maccli.view.view_generic.show("Applying configuration to %s" % instance['servername'])
            else:
                maccli.view.view_generic.clear()
                maccli.view.view_instance.show_instances(processing_instances)
                maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)

    if action:
        """ Allow all tasks to start """
        time.sleep(3)


def clean_up(instances, on_failure):
    failed = False
    for instance in instances:
        if instance['status'] == "Creation failed" or instance['status'] == "Configuration Error":
            failed = True

    if failed and on_failure is not None:
        maccli.view.view_generic.show_error("Cleaning up")
        for instance in instances:
            if on_failure == MACFILE_ON_FAILURE_DESTROY_OTHERS:
                if not (instance['status'] == "Creation failed" or instance['status'] == "Configuration Error"):
                    maccli.view.view_generic.show_error("Destroying instance %s " % instance['id'])
                    maccli.service.instance.destroy_instance(instance['id'])
            elif on_failure == MACFILE_ON_FAILURE_DESTROY_ALL:
                maccli.view.view_generic.show_error("Destroying instance %s " % instance['id'])
                maccli.service.instance.destroy_instance(instance['id'])
            else:
                maccli.view.view_generic.show_error("ERROR: clean up %s not implemented" % on_failure)

    return failed


def apply_resources(processed_instances, processed_resources, instances, roles, infrastructures, actions, resources, quiet):
    """ Apply all the resources that are not instances """
    # If event cannot happen, wait to the next loop
    resources_processed = []
    finish = True
    for infrastructure_key in infrastructures:
        infrastructure = infrastructures[infrastructure_key]

        if not any(infrastructure_key in d for d in processed_resources):
            maccli.logger.debug("%s does not exist in processed resources %s" % (infrastructure_key, processed_resources))
            if 'resource' in infrastructure:
                maccli.logger.debug("Type resource")
                log_type = "resource"
                key = infrastructure['resource']
                command_raw = resources[key]['create bash']
                if 'ready' in infrastructure:  # wait for the instance to be ready before proceeding
                    is_role_ready = maccli.helper.macfile.is_role_dependencies_ready(infrastructure, processed_instances, infrastructure_key)
                    if not is_role_ready: # we only change the variable if False is returned
                        finish = is_role_ready

            elif 'action' in infrastructure:
                maccli.logger.debug("Type action")
                log_type = "action"
                key = infrastructure['action']
                command_raw = actions[key]['bash']
                # TODO ssh not implemented
            elif 'role' in infrastructure:
                # if 'ready' in infrastructure:  # wait for the instance to be ready before proceeding
                #     section_finish = maccli.helper.macfile.wait_until_ready(infrastructure, processed_instances, infrastructure_key)
                #     if isinstance(section_finish, bool):
                #         finish = section_finish
                continue
            else:
                raise NotImplementedError

            if finish:  # if finish is false the process was aborted above
                maccli.logger.debug("%s %s command_raw: %s " % (log_type, key, command_raw))
                command_clean = command_raw
                is_parsed = True
                if maccli.helper.macfile.has_dependencies(command_raw, roles, infrastructures, actions):
                    maccli.logger.debug("Running %s %s with dependency, requested by infrastructure %s" % (log_type, key, infrastructure_key))
                    try:
                        command_clean, is_parsed = maccli.helper.macfile.parse_envs(command_raw, instances, roles, infrastructures, actions, processed_resources)
                    except InstanceDoesNotExistException as e:
                        raise MacResourceException("Instance %s  does not exist " % e, "Instance %s  does not exist " % e)
                else:
                    maccli.logger.debug("Running %s %s with no dependency, requested by infrastructure %s" % (log_type, key, infrastructure_key))

                if is_parsed:
                    rc, stdout, stderr = maccli.helper.cmd.run(command_clean)

                    if rc == 0:
                        if quiet:
                            maccli.view.view_generic.show("%s executed successfully" % infrastructure_key)
                        else:
                            maccli.view.view_generic.clear()
                            maccli.view.view_instance.show_instances(processed_instances)
                            maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures, processed_resources)
                        resources_processed.append({infrastructure_key: {'stderr': stderr, 'stdout': stdout, 'rc': rc, 'cmd': command_clean}})
                        if stdout:
                            maccli.logger.debug("STDOUT: %s " % stdout)
                        if stderr:
                            maccli.logger.debug("STDERR: %s " % stderr)
                    else:
                        if quiet:
                            maccli.view.view_generic.cmd_error(command_clean, rc, stdout, stderr)
                        else:
                            maccli.view.view_generic.clear()
                            maccli.view.view_instance.show_instances(processed_instances)
                            maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures, processed_resources)

                        raise MacResourceException("Error while executing resource %s " % infrastructure_key, {'stderr': stderr, 'stdout': stdout, 'rc': rc, 'cmd': command_clean})
                else:
                    finish = False
                    break  # exit from loop to avoid processing other resources

    return resources_processed, finish



