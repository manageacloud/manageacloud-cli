import helper.http


def get_list():
    status_code, json = helper.http.send_request("GET", "/instances")

    return json