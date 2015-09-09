__author__ = 'tk421'


def metadata_instance(macfile_root, infrastructure_key, role_key, role, infrastructure):
    """
    Generate the json metadata to create an instance
    """
    # version must be string
    macfile_root['version'] = str(macfile_root['version'])
    meta = macfile_root
    meta['macfile_role_name'] = role_key
    meta['macfile_infrastructure_name'] = infrastructure_key
    environment = get_environment(role, infrastructure)
    if environment is not None:
        meta['environment_raw'] = environment
    return meta


def metadata_resource(macfile_root, infrastructure_key, resource_name):
    """
    Generate the json metadata to create an instance
    """
    # version must be string
    macfile_root['version'] = str(macfile_root['version'])
    meta = macfile_root
    meta['macfile_resource_name'] = resource_name
    meta['macfile_infrastructure_name'] = infrastructure_key
    return meta


def get_environment(role, infrastructure):
    environment = None

    if 'environment' in role.keys():
        environment = role['environment']

    if 'environment' in infrastructure.keys():
        if environment is not None:
            environment = environment + infrastructure["environment"]
        else:
            environment = infrastructure["environment"]

    return environment