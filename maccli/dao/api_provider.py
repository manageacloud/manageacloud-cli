import maccli.helper.http


def get_locations(cookbook_tag, provider):
    status_code, json, raw = maccli.helper.http.send_request("GET",
                                                             "/provider/locations?cookbook_tag=%s&provider=%s" % (
                                                                 cookbook_tag, provider))

    return status_code, json


def get_hardwares(provider, location):
    status_code, json, raw = maccli.helper.http.send_request("GET", "/provider/hardware?provider=%s&location=%s" % (
        provider, location))

    if status_code == 400:
        if raw == "No credentials available":
            print ("")
            print ("There is no credentials available in your account for the provider %s" % (provider))
            print ("")
            print (
                "Please login in your account in %s and deploy a production server using the supplier %s" % (
                    maccli.domain, provider))
            print ("")
            print ("You just need to make this action once.")
            print ("")

    return status_code, json
