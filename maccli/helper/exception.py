class MacApiError(Exception):
    """An error status code was returned when querying the HTTP API"""
    pass


class MacAuthError(MacApiError):
    """An 401 Unauthorized status code was returned when querying the API"""
    pass


class MacParamValidationError(MacApiError):
    """There is an error when validating params for infrastructures"""
    pass


class MacParseEnvException(Exception):
    """Error while parsing variables in a macfile"""
    pass


class MacParseParamException(Exception):
    """Error while parsing params in a macfile"""
    pass


class MacResourceException(Exception):
    """Error while creating a resource"""
    pass


class InstanceDoesNotExistException(Exception):
    """The selected instance does not exist"""
    pass


class InstanceNotReadyException(Exception):
    """Instance is not ready"""
    pass


class MacErrorCreatingTier(Exception):
    """Error while parsing variables in a macfile"""
    pass


class FactError(Exception):
    """ Error in the Fact  """
    pass


class InternalError(RuntimeError):
    pass


class BashException(Exception):
    """Bash command failed running"""
    pass


class MacParameterNotFound(Exception):
    """Parameter has not been found"""
    pass

