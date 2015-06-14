import maccli.dao.api_provider
from maccli.config import RELEASE_ANY

def list_locations(cookbook_tag, provider_id, release):
    """
        List available instances in the account
    """
    server_status, raw_locations = maccli.dao.api_provider.get_locations(cookbook_tag, provider_id)

    if server_status == 404:
        print("Server configuration " + cookbook_tag + " not found")
        raw_locations = None

    clean_locations = []

    if release != RELEASE_ANY:
        for location in raw_locations:
            if location['release'] == release:
                clean_locations.append(location)
    else:
        clean_locations = raw_locations

    return clean_locations


def list_hardwares(provider, location, cookbook_tag, release):
    """
        List available hardware for given configuration
    """
    server_status, response = maccli.dao.api_provider.get_hardwares(provider, location, cookbook_tag, release)

    return response