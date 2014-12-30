from __future__ import print_function
import getpass
import ConfigParser
import sys
from os.path import join, expanduser

from prettytable import PrettyTable

import service.auth
import service.instance
from config import AUTH_SECTION, USER_OPTION, APIKEY_OPTION, MAC_FILE, EXCEPTION_EXIT_CODE


def login():
    username = raw_input("Username: ")
    password = getpass.getpass()

    try:
        user, api_key = service.auth.authenticate(username, password)
        if api_key is not None:
            config = ConfigParser.ConfigParser()
            config.add_section(AUTH_SECTION)
            config.set(AUTH_SECTION, USER_OPTION, user)
            config.set(AUTH_SECTION, APIKEY_OPTION, api_key)
            with open(join(expanduser('~'), MAC_FILE), 'w') as cfgfile:
                config.write(cfgfile)
            print("Login succeeded!")

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_list():
    try:
        json = service.instance.list_instances()
        pretty = PrettyTable(["Instance name", "Type", "Status"])

        if (len(json)):
            for instance in json:
                pretty.add_row([instance['servername'], instance['type'], instance['status']])
            print(pretty)
        else:
            print("There is no active instances")

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)