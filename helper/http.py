from urlparse import urljoin

from requests import Request, Session

from helper.exception import MacApiError, MacAuthError
import service


def get_auth_header():
    if service.user and service.apikey:
        return {'Authorization': 'ApiKey %s:%s' % (service.user, service.apikey)}
    else:
        return {}


def send_request(method, path, **kwargs):
    json = None
    url = urljoin(service.base_url, path.strip("/"))
    service.logger.info("%s %s %s" % (method, url, kwargs.get('data', '')))
    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': 'python-manageacloud/v%s' % service.__version__}
    headers.update(get_auth_header())
    # construct request
    s = Session()
    req = Request(method, url, headers=headers, **kwargs)
    # make the request
    response = s.send(req.prepare())
    status_code = getattr(response, 'status_code', None)
    service.logger.info("Status: %s", str(status_code))
    # handle the response
    if not status_code:
        # Most likely network trouble
        raise MacApiError("No Response (%s %s)" % (method, url))
    elif 200 <= status_code <= 299:
        # Success
        if status_code != 204:
            # Try to parse the response.
            try:
                json = response.json()
            except Exception:
                raise MacApiError("JSON Parse Error (%s %s). Response: %s" % (method, url, response.text))
        else:
            json = None
    else:
        # Server returned an error.
        if status_code == 403:
            raise MacAuthError("Not authorized")
        else:
            # TODO if verbose we should print this
            service.logger.warn("Status %s (%s %s). Response: %s" % (str(status_code), method, url, response.text))

    service.logger.info("Response: %s", json)
    return status_code, json