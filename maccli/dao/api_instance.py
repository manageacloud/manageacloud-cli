import json

import maccli.helper.http
from maccli.view.view_generic import show_error


def get_list():
    status_code, json, raw = maccli.helper.http.send_request("GET", "/instances")

    return json


def credentials(servername, session_id):

    serverorid = ""
    if servername is not None and servername != "":
        serverorid = servername
    elif session_id is not None and session_id != "":
        serverorid = session_id

    status_code, json_response, raw = maccli.helper.http.send_request("GET", "/credential/%s" % serverorid)

    if status_code == 404:
        show_error("Server not found")

    if status_code == 400:
        show_error("There is a problem with the input parametrs")

    return json_response


def create(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan, environments):
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
        'environments': environments
    }

    json_request = json.dumps(params)

    status_code, json_response, raw = maccli.helper.http.send_request("POST", "/instance", data=json_request)

    if status_code == 400:
        show_error("Error while building request: " + raw)

    if status_code == 409:
        show_error("Resources limit reached. If you need more resources please contact "
                   "sales@manageacloud.com. Detailed output:" + raw)

    return json_response


def destroy(servername, session_id):

    serverorid = ""
    if servername is not None and servername != "":
        serverorid = servername
    elif session_id is not None and session_id != "":
        serverorid = session_id

    status_code, json_response, raw = maccli.helper.http.send_request("DELETE", "/instance/%s" % serverorid)

    if status_code == 404:
        show_error("Server %s not found" % servername)

    if status_code == 400:
        show_error("Error with parameters: %s " % raw)

    return json_response
