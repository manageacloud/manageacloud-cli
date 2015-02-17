import time

import maccli.service.instance
from maccli.helper.network import is_ip_private, is_local
from maccli.helper.exception import MacParseEnvException, MacErrorCreatingTier


def parse_envs(role, roles_created):
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

    envs_raw = role['environment']
    envs_clean = []
    for en in envs_raw:
        key = en.keys()[0]
        val = en[key]
        if isinstance(val, basestring):
            if val.endswith(".PUBLIC_IP"):
                """
                    We substitute the value by the given role
                    Format existing_role.PROPERTY
                """
                role_name, property = val.split(".", 1)
                try:
                    if len(roles_created[role_name]) > 1:
                        ips = []
                        for instance in roles_created[role_name]:
                            instance_credentials = maccli.service.instance.credentials(None, instance['id'])
                            ips.append(instance_credentials['ip'])
                        envs_clean.append({key: ips})
                    else:
                        instance_credentials = maccli.service.instance.credentials(None, roles_created[role_name][0]['id'])
                        envs_clean.append({key: instance_credentials['ip']})
                except KeyError:
                    raise MacParseEnvException("Error while parsing env PUBLIC_IP", key, val)
            elif val.endswith(".PRIVATE_IP"):
                role_name, property = val.split(".", 1)
                try:
                    if len(roles_created[role_name]) > 1:
                        ips = []
                        for instance in roles_created[role_name]:
                            instance_facts = maccli.service.instance.facts(None, instance['id'])
                            ip = _get_private_ip_from_fatcs(instance_facts)
                            ips.append(ip)
                        envs_clean.append({key: ips})
                    else:
                        instance_facts = maccli.service.instance.facts(None, roles_created[role_name][0]['id'])
                        ip = _get_private_ip_from_fatcs(instance_facts)
                        envs_clean.append({key: ip})

                except KeyError:
                    raise MacParseEnvException("Error while parsing env PRIVATE_IP", key, val)

            elif ".FACT." in val:
                role_name, fact, property = val.split(".", 2)
                try:
                    if len(roles_created[role_name]) > 1:
                        properties = []
                        for instance in roles_created[role_name]:
                            instance_facts = maccli.service.instance.facts(None, instance['id'])
                            property_value = instance_facts[property.lower()]
                            properties.append(property_value)
                        envs_clean.append({key: properties})
                    else:
                        instance_facts = maccli.service.instance.facts(None, roles_created[role_name][0]['id'])
                        property_value = instance_facts[property.lower()]
                        envs_clean.append({key: property_value})

                except KeyError:
                    raise MacParseEnvException("Error while parsing env FACT", key, val)

            else:
                envs_clean.append(en)
        else:
            envs_clean.append(en)

    role['environment'] = envs_clean

    return role


def _get_private_ip_from_fatcs(facts):
    ip = ""
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

    return ip


def create_tier(role, infrastructure):
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
        instance = maccli.service.instance.create_instance(role["configuration"], role["deployment"],
                                                           infrastructure["location"], role["name"],
                                                           infrastructure["provider"],
                                                           role["release"], role["branch"], hardware, lifespan,
                                                           environment, hd)
        instances.append(instance)
        print "Instance '%s' created, status '%s'" % (instance['id'], instance['status'])

    wait = True
    pending_instances = len(instances)
    while wait:
        time.sleep(10)
        instance_status = maccli.service.instance.list_instances()
        instances_created = 0
        for instance in instances:
            for ie in instance_status:
                if ie['id'] == instance['id']:

                    print "Instance '%s' status '%s'" % (ie['id'], ie['status'])

                    if ie['status'].find("Ready") <> -1:
                        instances_created += 1

                    if ie['status'].find("failed") <> -1:
                        raise MacErrorCreatingTier("Instance %s failed. Aborting. No automatic clean-up, please revert " \
                                                   "all the changes manually.")

        if wait:
            if pending_instances - instances_created == 0:
                wait = False
            else:
                print "[%s/%s] Waiting instances to be created" % (instances_created, pending_instances)

    return instances