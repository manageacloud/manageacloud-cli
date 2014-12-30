class MacApiError(Exception):
    """An error status code was returned when querying the HTTP API"""
    pass


class MacAuthError(MacApiError):
    """An 401 Unauthorized status code was returned when querying the API"""
    pass


class InternalError(RuntimeError):
    pass