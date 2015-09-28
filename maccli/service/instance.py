import os
import tempfile
import time

import pexpect

import maccli.dao.api_instance
import maccli.helper.cmd
import maccli.helper.simplecache
import maccli.helper.metadata
from maccli.helper.exception import InstanceDoesNotExistException, InstanceNotReadyException


def list_instances(name_or_ids = None):
    """
        List available instances in the account
    """
    instances = []
    instances_raw = maccli.dao.api_instance.get_list()
    if name_or_ids is not None:

        # if name_or_ids is string, convert to list
        if isinstance(name_or_ids, basestring):
            name_or_ids = [name_or_ids]

        for instance_raw in instances_raw:
            if instance_raw['servername'] in name_or_ids or instance_raw['id'] in name_or_ids:
                instances.append(instance_raw)
    else:
        instances = instances_raw

    return instances


def list_by_infrastructure(name, version):
    instances = maccli.dao.api_instance.get_list()
    filtered_instances = []
    for instance in instances:
        if 'metadata' in instance and 'infrastructure' in instance['metadata'] and 'name' in instance['metadata'][
            'infrastructure']:
            infrastructure_name = instance['metadata']['infrastructure']['name']
        else:
            infrastructure_name = ""

        if 'metadata' in instance and 'infrastructure' in instance['metadata'] and 'version' in instance['metadata'][
            'infrastructure']:
            infrastructure_version = instance['metadata']['infrastructure']['version']
        else:
            infrastructure_version = ""

        if infrastructure_name == name and infrastructure_version == version:
            filtered_instances.append(instance)

    return filtered_instances


def ssh_command_instance(instance_id, cmd):

    rc, stdout, stderr = -1, "", ""
    cache_hash = maccli.helper.simplecache.hash_value(cmd)
    cache_key = 'ssh_%s_%s' % (instance_id, cache_hash)
    cached_value = maccli.helper.simplecache.get(cache_key)  # read from cache

    if cached_value is not None:
        rc = cached_value['rc']
        stdout = cached_value['stdout']
        stderr = cached_value['stderr']
    else:

        instance = maccli.dao.api_instance.credentials(instance_id)

        if instance is None:
            raise InstanceDoesNotExistException(instance_id)

        if not (instance['privateKey'] or instance['password']):
            raise InstanceNotReadyException(instance_id)

        if instance is not None and (instance['privateKey'] or instance['password']):
            if instance['privateKey']:
                tmp_fpath = tempfile.mkstemp()
                try:
                    with open(tmp_fpath[1], "wb") as f:
                        f.write(bytes(instance['privateKey']))

                    command = "ssh %s@%s -i %s %s" % (instance['user'], instance['ip'], f.name, cmd)
                    rc, stdout, stderr = maccli.helper.cmd.run(command)

                finally:
                    os.remove(tmp_fpath[1])
            else:
                """ Authentication with password """
                command = "ssh %s@%s %s" % (instance['user'], instance['ip'], cmd)
                child = pexpect.spawn(command)
                i = child.expect(['.* password:', "yes/no"], timeout=120)
                if i == 1:
                    child.sendline("yes")
                    child.expect('.* password:', timeout=120)

                child.sendline(instance['password'])
                child.expect(pexpect.EOF, timeout=120)
                output = child.before

                while child.isalive():
                    time.sleep(0.1)

                rc = child.exitstatus

                # HACK: we do not really capture stderr
                if rc:
                    stdout = ""
                    stderr = output
                else:
                    stdout = output
                    stderr = ""

        # save cache
        if not rc:
            cached_value = {
                'rc': rc,
                'stdout': stdout,
                'stderr': stderr
            }
            maccli.helper.simplecache.set_value(cache_key, cached_value)

    return rc, stdout, stderr


def ssh_interactive_instance(instance_id):
    """
        ssh to an existing instance for an interactive session
    """
    stdout = None
    instance = maccli.dao.api_instance.credentials(instance_id)

    if instance is not None:

        if instance['privateKey']:
            """ Authentication with private key """
            tmp_fpath = tempfile.mkstemp()
            try:
                with open(tmp_fpath[1], "wb") as f:
                    f.write(bytes(instance['privateKey']))

                command = "ssh %s@%s -i %s " % (instance['user'], instance['ip'], f.name)
                os.system(command)

            finally:
                os.remove(tmp_fpath[1])

        else:
            """ Authentication with password """
            command = "ssh %s@%s" % (instance['user'], instance['ip'])
            child = pexpect.spawn(command)
            i = child.expect(['.* password:', "yes/no"], timeout=60)
            if i == 1:
                child.sendline("yes")
                child.expect('.* password:', timeout=60)

            child.sendline(instance['password'])
            child.interact()

    return stdout

def create_instance(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port, net, metadata=None, applyChanges=True):
    """
        List available instances in the account
    """
    return maccli.dao.api_instance.create(cookbook_tag, deployment, location, servername, provider, release, branch,
                                          hardware, lifespan, environments, hd, port, net, metadata, applyChanges)


def destroy_instance(instanceid):
    """

    Destroy the server

    :param servername:
    :return:
    """
    return maccli.dao.api_instance.destroy(instanceid)


def credentials(servername, session_id):
    """

    Gets the server credentials: public ip, username, password and private key

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.credentials(servername, session_id)


def facts(instance_id):
    """

    Returns facts about the system

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.facts(instance_id)


def log(instance_id):
    """

    Returns server logs

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.log(instance_id)


def lifespan(instance_id, amount):
    """

    Set new instance lifespan

    :param instance_id;
    :return:
    """
    return maccli.dao.api_instance.update(instance_id, amount)


def update_configuration(cookbook_tag, instance_id, new_metadata=None):
    """
    Update server configuration with given cookbook

    :param cookbook_tag:
    :param instance_id:
    :return:
    """

    return maccli.dao.api_instance.update_configuration(cookbook_tag, instance_id, new_metadata)


def create_instances_for_role(root, infrastructure, roles, infrastructure_key, quiet):
    """ Create all the instances for the given tier """

    maccli.logger.debug("Processing infrastructure %s" % infrastructure_key)

    roles_created = {}
    maccli.logger.debug("Type role")
    infrastructure_role = infrastructure['role']

    role_raw = roles[infrastructure_role]["instance create"]
    metadata = maccli.helper.metadata.metadata_instance(root, infrastructure_key, infrastructure_role, role_raw,
                        infrastructure)
    instances = create_tier(role_raw, infrastructure, metadata, quiet)
    roles_created[infrastructure_role] = instances

    return roles_created


def create_tier(role, infrastructure, metadata, quiet):
    """
        Creates the instances that represents a role in a given infrastructure

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

    environment = maccli.helper.metadata.get_environment(role, infrastructure)

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

    net = None
    try:
        net = infrastructure["net"]
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
        instance = maccli.dao.api_instance.create(role["configuration"], deployment,
                                                  infrastructure["location"], infrastructure["name"],
                                                  provider, release, branch, hardware, lifespan,
                                                  environment, hd, port, net, metadata, False)
        instances.append(instance)
        maccli.logger.info("Creating instance '%s'" % (instance['id']))

    return instances
