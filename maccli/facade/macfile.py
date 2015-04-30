from __future__ import print_function
import time

import pprint

import maccli.service.instance
from maccli.helper.network import is_ip_private, is_local
from maccli.helper.exception import MacParseEnvException, FactError

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


def create_tier(role, infrastructure, metadata):
    """
        Creates tje instances that represents a role in a given infrastructure

    :param role:
    :param infrastructure:
    :return:
    """

    lifespan = None
    try:
        lifespan = role['lifespan']
    except KeyError:
        pass

    hardware = ""
    try:
        hardware = infrastructure["hardware"]
    except KeyError:
        pass

    environment = None
    try:
        environment = role["environment"]
    except KeyError:
        pass

    hd = None
    try:
        hd = role["hd"]
    except KeyError:
        pass

    instances = []
    for x in range(0, infrastructure['amount']):
        instance = maccli.service.instance.create_instance(role["configuration"], infrastructure["deployment"],
                                                           infrastructure["location"], infrastructure["name"],
                                                           infrastructure["provider"],
                                                           infrastructure["release"], role["branch"], hardware, lifespan,
                                                           environment, hd, metadata, False)
        instances.append(instance)
        print ("Creating instance '%s'" % (instance['id']))
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

                        if instance_role_name == role_name:
                            ip = instance['ipv4']
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

                        if instance_role_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(None, instance['id'])
                                ip = _get_private_ip_from_fatcs(instance_facts)
                                ips.append(ip)
                            except FactError:
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

                        if instance_role_name == role_name:
                            try:
                                instance_facts = maccli.service.instance.facts(None, instance['id'])
                                property_value = instance_facts[property.lower()]
                                facts.append(property_value)
                            except FactError:
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

def apply_infrastructure_changes(instances):
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
        else:
            other_instances.append(instance)

    action = False
    for instance in configuration_pending:
            cookbook_tag = instance['metadata']['system']['role']['cookbook_tag']
            instance_id = instance['id']
            if 'environment_raw' in instance['metadata']['infrastructure']:
                environment_raws = instance['metadata']['infrastructure']['environment_raw']
                environment_clean, processed = parse_instance_envs(environment_raws, other_instances)
                metadata_new = {'system': {'role': {'environment': environment_clean}}}
                if processed:
                    action = True
                    maccli.service.instance.update_configuration(cookbook_tag, instance_id, metadata_new)
            else:
                action = True
                maccli.service.instance.update_configuration(cookbook_tag, instance_id)

    if action:
        """ Allow all tasks to start """
        time.sleep(3)