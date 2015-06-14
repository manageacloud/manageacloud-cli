from __future__ import print_function
import time
import maccli

import pprint
from maccli.config import MACFILE_ON_FAILURE_DESTROY_OTHERS, MACFILE_ON_FAILURE_DESTROY_ALL
import maccli.service.instance
import maccli.view.view_generic
import maccli.view.view_instance
from maccli.helper.network import is_ip_private, is_local
from maccli.helper.exception import MacParseEnvException, FactError, MacApiError

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
                environment = dict(environment.items() + role["environment"].items())
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
                    for instance in instances:
                        instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
                        instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']

                        if instance_role_name == role_name or instance_infrastructure_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(instance['id'])
                                ip = _get_private_ip_from_fatcs(instance_facts)
                                ips.append(ip)
                            except FactError:
                                pass
                            except MacApiError:
                                pass

                    if len(ips) > 0:
                        envs_clean[key] = ips
                    else:
                        all_processed = False

                except KeyError:
                    raise MacParseEnvException("Error while parsing env PRIVATE_IP", key, val)

            elif ".FACT." in val:
                role_name, fact, property = val.split(".", 2)

                try:
                    facts = []
                    for instance in instances:
                        instance_role_name = instance['metadata']['infrastructure']['macfile_role_name']
                        instance_infrastructure_name = instance['metadata']['infrastructure']['macfile_infrastructure_name']

                        if instance_role_name == role_name or instance_infrastructure_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(instance['id'])
                                property_value = instance_facts[property.lower()]
                                facts.append(property_value)
                            except FactError:
                                pass
                            except MacApiError:
                                pass

                    if len(facts) > 0:
                        envs_clean[key] = facts
                    else:
                        all_processed = False

                except KeyError:
                    raise MacParseEnvException("Error while parsing env PRIVATE_IP", key, val)

            else:
                envs_clean[key] = val

    return envs_clean, all_processed


def apply_infrastructure_changes(instances, infrastructure_name, version, quiet):
    """
    Make sure that all instances in a infrastructure are processed
    :param instances:
    :return:
    """
    configuration_pending = []
    other_instances = []
    for instance in instances:

        if instance['status'] == "Instance completed":
            configuration_pending.append(instance)

        if instance['ipv4'] is not None:
            other_instances.append(instance)

    action = False
    for instance in configuration_pending:
        maccli.logger.debug("[%s] Checking instance " % instance['servername'])
        cookbook_tag = instance['metadata']['system']['role']['cookbook_tag']
        instance_id = instance['id']
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