import maccli.dao.api_configuration


def list_configurations():
    """
        List available configurations for the current user
    """

    server_status, response = maccli.dao.api_configuration.get_user_configuration()

    return response


def search_configurations(keywords):
    """
        List available configurations for the current user
    """

    server_status, response = maccli.dao.api_configuration.search_public_configuration(keywords)

    return response


