import service
import dao.api_auth


def is_authenticated():
    """Returns whether the manageacloud user and apikey are set

    :returns: bool -- whether the manageacloud user and apikey are set
    """
    return service.user is not None and service.apikey is not None


def logout():
    """Sets the manageacloud user and apikey to None"""
    service.user = None
    service.apikey = None


def authenticate(username, password):
    """Authenticates a Manageacloud user using username and password.

    :param username: The username of the user to authenticate
    :type username: str.
    :param password: The password of the user to authenticate
    :type password: str.
    :raises: MacAuthError
    """
    user, apikey = dao.api_auth.get_auth(username, password)

    if user:
        service.user = user
    if apikey:
        service.apikey = apikey

    return user, apikey