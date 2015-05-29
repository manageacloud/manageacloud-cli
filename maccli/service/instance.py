import os
import tempfile

import pexpect

import maccli.dao.api_instance


def list_instances():
    """
        List available instances in the account
    """
    return maccli.dao.api_instance.get_list()


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


def ssh_instance(instance_id, cmd=None):
    """
        ssh to an existing instance
    """
    instance = maccli.dao.api_instance.credentials(instance_id)

    if instance is not None:

        command_str = ""
        if cmd is not None:
            command_str = "%s" % cmd

        if instance['privateKey']:
            """ Authentication with private key """
            tmp_fpath = tempfile.mkstemp()
            try:
                with open(tmp_fpath[1], "wb") as f:
                    f.write(bytes(instance['privateKey']))
                command = "ssh %s@%s -i %s %s" % (instance['user'], instance['ip'], f.name, command_str)
                os.system(command)
            finally:
                os.remove(tmp_fpath[1])

        else:
            """ Authentication with password """
            command = "ssh %s@%s %s" % (instance['user'], instance['ip'], command_str)
            child = pexpect.spawn(command)
            i = child.expect(['.* password:', "yes/no"], timeout=60)
            if i == 1:
                child.sendline("yes")
                child.expect('.* password:', timeout=60)

            child.sendline(instance['password'])
            child.interact()


def create_instance(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port, metadata=None, applyChanges=True):
    """
        List available instances in the account
    """
    return maccli.dao.api_instance.create(cookbook_tag, deployment, location, servername, provider, release, branch,
                                          hardware, lifespan, environments, hd, port, metadata, applyChanges)


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


def metadata(macfile_root, infrastructure_key, role_key, role):
    """
    Generate the json metadata to create an instance
    """
    meta = macfile_root
    meta['macfile_role_name'] = role_key
    meta['macfile_infrastructure_name'] = infrastructure_key
    if 'environment' in role.keys():
        meta['environment_raw'] = role['environment']
    return meta


def update_configuration(cookbook_tag, instance_id, new_metadata=None):
    """
    Update server configuration with given cookbook

    :param cookbook_tag:
    :param instance_id:
    :return:
    """

    return maccli.dao.api_instance.update_configuration(cookbook_tag, instance_id, new_metadata)