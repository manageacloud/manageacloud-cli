import maccli.dao.api_infrastructure
import maccli.dao.api_instance
import maccli


def list_infrastructure():
    """
        List available infrastructure
    """

    server_status, response = maccli.dao.api_infrastructure.get_infrastructure_list()

    return response


def search_instances(name, version):
    """
        Search infrastructure by name and version
    """

    server_status, response = maccli.dao.api_infrastructure.search_infrastructure(name, version)

    return response


def lifespan(amount, name, input_version):
    """
        Manipulate's lifespan for all server in a infrastructure
    """

    server_status, infrastructure = maccli.dao.api_infrastructure.search_infrastructure(name, input_version)

    new_infrastructure = []
    if len(infrastructure):
        for inf in infrastructure:
            if name is None or name == inf['name']:
                for version in inf['versions']:
                    if input_version is None or input_version == version:
                        instances = []
                        for instance in inf['cloudServers']:
                            if instance['type'] == 'testing':
                                maccli.logger.debug("Adding %s to instance %s" % (amount, instance['id']))
                                new_instance = maccli.dao.api_instance.update(instance['id'], amount)
                                instances.append(new_instance)
                        inf['cloudServers'] = instances
                        new_infrastructure.append(inf)

    return new_infrastructure



