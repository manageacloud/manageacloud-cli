import maccli.helper.http
from maccli.config import RELEASE_ANY


def get_locations(cookbook_tag, provider):
    status_code, json, raw = maccli.helper.http.send_request("GET",
                                                             "/provider/locations?cookbook_tag=%s&provider=%s" % (
                                                                 cookbook_tag, provider))

    return status_code, json


def get_hardwares(provider, location, cookbook_tag, release):

    if release is None or release == "":
        release = RELEASE_ANY

    status_code, json, raw = maccli.helper.http.send_request("GET",
                                                             "/provider/hardware?provider=%s&location=%s&release=%s&cookbook_tag=%s" %
                                                             (provider, location, release, cookbook_tag))

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
