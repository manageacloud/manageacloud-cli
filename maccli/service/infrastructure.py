import maccli.dao.api_infrastructure


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

    server_status, response = maccli.dao.api_infrastructure.search_instances(name, version)

    return response


