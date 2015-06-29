from urlparse import urljoin
from httplib2 import Http
import json
from urllib import urlencode

from maccli.helper.exception import MacApiError, MacAuthError
import maccli


def get_auth_header(auth = None):
    if auth is None:
        if maccli.user and maccli.apikey:
            return {'Authorization': 'ApiKey %s:%s' % (maccli.user, maccli.apikey)}
        else:
            return {}
    else:
        return {'Authorization': 'Basic %s' % auth}


def send_request(method, path, auth=None, data=None, **kwargs):
    json_content = None
    url = urljoin(maccli.base_url, path.strip("/"))
    maccli.logger.info("%s %s %s" % (method, url, kwargs.get('data', '')))
    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': 'python-manageacloud/v%s' % maccli.__version__}
    headers.update(get_auth_header(auth))
    # make the request
    h = Http()
    resp, content = h.request(url, method, headers=headers, body=data, **kwargs)
    # handle the response
    status_code = getattr(resp, 'status', None)
    maccli.logger.info("Status: %s", str(status_code))
    if not status_code:
        # Most likely network trouble
        raise MacApiError("No Response (%s %s)" % (method, url))
    elif 200 <= status_code <= 299:
        # Success
        if status_code != 204:
            # Try to parse the response.
            try:
                json_content = json.loads(content)
            except Exception:
                raise MacApiError("JSON Parse Error (%s %s). Response: %s" % (method, url, content))
        else:
            json_content = None
    else:
        # Server returned an error.
        if status_code == 403:
            raise MacAuthError("Not authorized")
        elif status_code == 503:
            maccli.logger.info("Status %s (%s %s). Response: %s" % (str(status_code), method, url, content))
        else:
            maccli.logger.warn("Status %s (%s %s). Response: %s" % (str(status_code), method, url, content))

    maccli.logger.info("Response: %s", json_content)
    return status_code, json_content, content