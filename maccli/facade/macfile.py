import time
import maccli.service.instance

def parse_envs(role, roles_created):


    """
        Replaces the values in the environment variables for values
        that exist in this infrastructure

        Supported:

         - role.PUBLIC_IP -> adds the public ip

    :param role:
    :param roles_created:
    :return:
    """

    envs_raw = role['environment']
    envs_clean  = []
    for en in envs_raw:
        key = en.keys()[0]
        val = en[key]
        if val.endswith(".PUBLIC_IP"):
            """
                We substitute the value by the given role
                Format existing_role.PROPERTY
            """
            role_name, property = val.split(".", 1)
            if len(roles_created[role_name]) > 1:
                ips = []
                for instance in roles_created[role_name]:
                    instance_credentials = maccli.service.instance.credentials(None, instance['id'])
                    ips.append(instance_credentials['ip'])
                envs_clean.append({key:ips})
            else:
                instance_credentials = maccli.service.instance.credentials(None, roles_created[role_name][0]['id'])
                envs_clean.append({key:instance_credentials['ip']})
        else:
            envs_clean.append(en)
    role['environment'] = envs_clean

    return role

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

    instances = []
    for x in range(0, infrastructure['amount']):
        instance = maccli.service.instance.create_instance(role["configuration"], role["deployment"], infrastructure["location"], role["name"],infrastructure["provider"],
                                                    role["release"], role["branch"], hardware, lifespan, environment)
        instances.append(instance)
        print "Instance '%s' created, status '%s'" % (instance['id'], instance['status'])

    wait = True
    failed = False
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
                        print "ERROR: Instance %s failed. Aborting. No automatic clean-up, please revert " \
                              "all the changes manually."
                        failed = True
                        wait =False

        if wait:
            if pending_instances - instances_created == 0:
                wait = False
            else:
                print "[%s/%s] Waiting instances to be created" % (instances_created, pending_instances)

    return instances, failed