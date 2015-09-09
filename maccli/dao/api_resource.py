import json

import maccli.helper.http
from maccli.view.view_generic import show_error


def get_list():
    status_code, json, raw = maccli.helper.http.send_request("GET", "/resources")
    return json


def create(name, create_bash, rc, stderr, stdout, destroy_bash, metadata):
    """
     Creates a new resource
    """
    params = {
        'name': name,
        'create_cmd': create_bash,
        'create_rc': rc,
        'create_stderr': stderr,
        'create_stdout': stdout,
        'destroy_cmd': destroy_bash,
        'metadata': json.dumps(metadata),
    }

    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("POST", "/resource", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    return json_response


def update(resource):

    json_request = json.dumps(resource)

    status_code, json_response, raw = maccli.helper.http.send_request("PUT", "/resource", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    return json_response


def delete(resource):

    json_request = json.dumps(resource)

    status_code, json_response, raw = maccli.helper.http.send_request("DELETE", "/resource", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    return json_response