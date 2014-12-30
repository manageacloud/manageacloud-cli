from requests.auth import HTTPBasicAuth


def get_list(auth_header):

    auth = HTTPBasicAuth(username, password)
    status_code, json = mac.http.send_request("GET", "/user/auth", auth=auth)
    user = username
    apikey = None
    if json:
        user = json.get('username', None)
        apikey = json.get('apiKey', None)
    return user, apikey