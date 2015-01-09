def list_locations(cookbook_tag, provider_id):
    """
        List available instances in the account
    """
    server_status, response = dao.api_provider.get_locations(cookbook_tag, provider_id)

    if server_status == 404:
        print("Server configuration " + cookbook_tag + " not found")
        response = None

    return response


def list_hardwares(provider_id, location_id):
    """
        List available hardware for given configuration
    """
    server_status, response = dao.api_provider.get_hardwares(provider_id, location_id)

    return response