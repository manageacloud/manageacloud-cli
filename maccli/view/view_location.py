from __future__ import print_function
from prettytable import PrettyTable


def show_locations(locations):
    pretty = PrettyTable(["Distribution", "Location", "Description"])
    pretty.align["Description"] = "l"
    for location in locations:
        pretty.add_row([location['release'], location['id'], location['description']])

    print(pretty)
