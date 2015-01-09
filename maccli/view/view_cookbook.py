from prettytable import PrettyTable


def show_configurations(cookbooks):
    pretty = PrettyTable(["Tag", "Title", "Summary"])
    pretty.align = "l"
    if len(cookbooks):
        for cookbook in cookbooks:
            pretty.add_row([cookbook['tag'], cookbook['name'], cookbook['summary']])

        print(pretty)
        print("")
        print("Search more at https://manageacloud.com/cookbooks")
        print("")
    else:
        print("There are not configurations available")


def show_configurations_url(cookbooks):
    pretty = PrettyTable(["Tag", "Url"])
    pretty.align = "l"
    if len(cookbooks):
        for cookbook in cookbooks:
            pretty.add_row([cookbook['tag'], cookbook['url']])

        print(pretty)
        print("")
        print("Search more at https://manageacloud.com/cookbooks")
        print("")
    else:
        print("There are not configurations available")


def show_configurations_help():
    print("Show more help:")
    print("")
    print("    mac configuration -h")
    print("")
