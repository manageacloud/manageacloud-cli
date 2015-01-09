from urlparse import urljoin

from requests import Request, Session

from maccli.helper.exception import MacApiError, MacAuthError
import maccli


def get_auth_header():
    if maccli.user and maccli.apikey:
        return {'Authorization': 'ApiKey %s:%s' % (maccli.user, maccli.apikey)}
    else:
        return {}


def send_request(method, path, **kwargs):
    json = None
    url = urljoin(maccli.base_url, path.strip("/"))
    maccli.logger.info("%s %s %s" % (method, url, kwargs.get('data', '')))
    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': 'python-manageacloud/v%s' % maccli.__version__}
    headers.update(get_auth_header())
    # construct request
    s = Session()
    req = Request(method, url, headers=headers, **kwargs)
    # make the request
    response = s.send(req.prepare())
    status_code = getattr(response, 'status_code', None)
    maccli.logger.info("Status: %s", str(status_code))
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
            maccli.logger.warn("Status %s (%s %s). Response: %s" % (str(status_code), method, url, response.text))

    maccli.logger.info("Response: %s", json)
    return status_code, json, response.text