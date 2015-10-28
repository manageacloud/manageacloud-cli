import os
import maccli.dao.api_provider
from maccli.config import RELEASE_ANY
from maccli.view.view_generic import show_error, show


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


def save_credentials(provider, client, key_raw, force_file):
    """

    Save the credentials if are valid

    :param provider:
    :param client:
    :param key: Is an string of a file path
    :return:
    """
    if os.path.isfile(key_raw) or force_file:
        maccli.logger.info("%s is an existing path, opening file" % key_raw)
        with open(key_raw, "r") as myfile:
            key = myfile.read()
            maccli.logger.debug("%s read, contents are:\n%s" % (key_raw, key))
    else:
        key = key_raw

    server_status, response = maccli.dao.api_provider.credentials(provider, client, key)

    if server_status == 409:
        show_error("The credentials provided has been rejected by the supplier. Please make sure that you are using a correct 'clientid' and 'key'")

    if server_status == 200:
        show("Credentials validated and saved. The provider '%s' has been activated." % provider)

    return response
