import json

import maccli.helper.http


def get_user_configuration():

    status_code, json, raw = maccli.helper.http.send_request("GET", "/configuration/list")

    return status_code, json

def search_public_configuration(keywords):

    params = {
        'keyword': keywords
    }
    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/configuration/search", data=json_request)

    return status_code, json_response

