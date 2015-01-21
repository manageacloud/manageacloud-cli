import urllib

import maccli.helper.http


def get_user_configuration():
    status_code, json, raw = maccli.helper.http.send_request("GET", "/configuration/list")

    return status_code, json


def search_public_configuration(keywords):

    querystring = ""
    if keywords is not None and len(keywords):
        params = {
            'keyword': keywords
        }
        querystring = "?" + urllib.urlencode(params, True)

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/configuration/search%s" % querystring)

    return status_code, json_response

