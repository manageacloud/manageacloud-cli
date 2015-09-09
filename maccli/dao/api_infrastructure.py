import urllib

import maccli.helper.http


def get_infrastructure_list():
    status_code, json, raw = maccli.helper.http.send_request("GET", "/infrastructure")

    return status_code, json


def search_infrastructure(name, version):

    params = {}
    if name is not None:
        params['name'] = name

    if version is not None:
        params['version'] = version

    querystring = "?" + urllib.urlencode(params, True)

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/infrastructure%s" % querystring)

    return status_code, json_response

