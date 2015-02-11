class MacApiError(Exception):
    """An error status code was returned when querying the HTTP API"""
    pass


class MacAuthError(MacApiError):
    """An 401 Unauthorized status code was returned when querying the API"""
    pass

class MacParseEnvException(Exception):
    """Error while parsing variables in a macfile"""
    pass

class MacErrorCreatingTier(Exception):
    """Error while parsing variables in a macfile"""
    pass



class InternalError(RuntimeError):
    pass