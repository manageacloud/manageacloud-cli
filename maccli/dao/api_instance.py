import json

import maccli.helper.http
from maccli.view.view_generic import show_error


def get_list():
    status_code, json, raw = maccli.helper.http.send_request("GET", "/instances")

    return json


def credentials(instance_id):

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/credential/%s" % instance_id)

    if status_code == 404:
        show_error("Server not found")

    if status_code == 400:
        show_error("There is a problem with the input parametrs")

    return json_response


def create(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
           environments, hd, port, net, metadata, applyChanges):
    """
     Creates a new instance

    :param cookbook_tag:
    :param deployment:
    :param location:
    :param servername:
    :param provider:
    :param release:
    :param branch:
    :param hardware:
    :param lifespan:
    :param environments:
    :param hd:
    :return:
    """

    params = {
        'cookbook_tag': cookbook_tag,
        'deployment': deployment,
        'location': location,
        'servername': servername,
        'provider': provider,
        'release': release,
        'branch': branch,
        'hardware': hardware,
        'lifespan': lifespan,
        'environments': environments,
        'hd': hd,
        'port': port,
        'net': net,
        'metadata': json.dumps(metadata),
        'apply_changes': applyChanges
    }

    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("POST", "/instance", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    if status_code == 409:
        show_error("Resources limit reached. If you need more resources please contact "
                   "sales@manageacloud.com. Detailed output:" + raw)

    return json_response


def update_configuration(cookbook_tag, instance_id, new_metadata):
    """
     Creates a new instance

    :param cookbook_tag:
    :param instance_id:
    :return:
    """

    params = {
        'cookbook_tag': cookbook_tag,
        'instance_id': instance_id,
        'metadata': new_metadata
    }

    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("PUT", "/instance", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    if status_code == 404:
        show_error("Error while building request: " + raw)

    if status_code == 401:
        show_error("Error while building request: " + raw)

    return json_response


def destroy(instanceid):

    status_code, json_response, raw = maccli.helper.http.send_request("DELETE", "/instance/%s" % instanceid)

    if status_code == 404:
        show_error("Server %s not found" % instanceid)

    if status_code == 400:
        show_error("Error with parameters: %s " % raw)

    return json_response


def facts(instance_id):

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/facts/%s" % instance_id)

    if status_code == 404:
        show_error("Server not found")

    if status_code == 400:
        show_error("There is a problem with the input parameters")

    return json_response


def log(instance_id):

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/log/%s" % instance_id)

    if status_code == 404:
        show_error("Server not found")

    if status_code == 400:
        show_error("There is a problem with the input parameters")

    return json_response


def update(instance_id, lifespan):

    params = {
        'lifespan': lifespan
    }

    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("PUT", "/instance/%s" % instance_id,
                                                                      data=json_request)

    if status_code == 404:
        show_error("Server not found")

    if status_code == 400:
        show_error("There is a problem with the input parameters")

    return json_response