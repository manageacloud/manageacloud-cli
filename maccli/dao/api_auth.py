import os
import ConfigParser

import base64
import maccli.helper.http


def get_auth(username, password):
    """Returns the user's Username and ApiKey, or raises an exception if username/password incorrect

    :param username: The email of the user to authenticate
    :type username: str
    :param password: The password of the user to authenticate
    :type password: str
    :raises: MacApiError
    :returns: str, str -- the Username, ApiKey to use for the given username/email
    """
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    status_code, json, raw = maccli.helper.http.send_request("GET", "/user/auth", auth=base64string)
    user = username
    apikey = None
    if json:
        user = json.get('username', None)
        apikey = json.get('apiKey', None)
    return user, apikey


def load_from_file(file="~/.manageacloud"):
    """Attempts to read manageacloud credentials from a config file and return a tuple of (user, apikey)

    :param file: The filename where Manageacloud auth config is stored
    :type file: str
    :returns: tuple -- tuple of (user, apikey) if config found and valid, (None, None) otherwise
    """
    try:
        cfgfile = os.path.expanduser(file)
        cp = ConfigParser.ConfigParser()
        cp.read(cfgfile)
        return cp.get("auth", "user"), cp.get("auth", "apikey")
    except ConfigParser.Error:
        return None, None