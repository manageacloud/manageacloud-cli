from __future__ import print_function
import maccli
from prettytable import PrettyTable


def show_configurations(cookbooks):
    pretty = PrettyTable(["Tag", "Title", "Summary"])
    pretty.align = "l"
    if len(cookbooks):
        for cookbook in cookbooks:
            pretty.add_row([cookbook['tag'], cookbook['name'], cookbook['summary']])

        print(pretty)
        print("")
        print("Search more at %s/cookbooks" % maccli.domain)
        print("")
    else:
        print("There are not configurations available")
        print("")
        print("You can create a new server configuration at %s" % maccli.domain)


def show_configurations_url(cookbooks):
    pretty = PrettyTable(["Tag", "Url"])
    pretty.align = "l"
    if len(cookbooks):
        for cookbook in cookbooks:
            pretty.add_row([cookbook['tag'], cookbook['url']])

        print(pretty)
        print("")
        print("Search more at %s/cookbooks" % maccli.domain)
        print("")
    else:
        print("There are not configurations available")
        print("")
        print("You can create a new server configuration at %s" % maccli.domain)


def show_configurations_help():
    print("Show more help:")
    print("")
    print("    mac configuration -h")
    print("")



