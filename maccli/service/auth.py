import maccli.service
import maccli.dao.api_auth


def is_authenticated():
    """Returns whether the manageacloud user and apikey are set

    :returns: bool -- whether the manageacloud user and apikey are set
    """
    return maccli.user is not None and maccli.apikey is not None


def logout():
    """Sets the manageacloud user and apikey to None"""
    maccli.user = None
    maccli.apikey = None


def authenticate(username, password):
    """Authenticates a Manageacloud user using username and password.

    :param username: The username of the user to authenticate
    :type username: str.
    :param password: The password of the user to authenticate
    :type password: str.
    :raises: MacAuthError
    """
    user, apikey = maccli.dao.api_auth.get_auth(username, password)

    if user:
        maccli.user = user
    if apikey:
        maccli.apikey = apikey

    return user, apikey