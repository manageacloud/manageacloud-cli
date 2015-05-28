from __future__ import print_function
from prettytable import PrettyTable
import maccli


def show_infrastructure(infrastructure):
    pretty = PrettyTable(["Infrastructure name", "version"])
    if len(infrastructure):
        for inf in infrastructure:
            for version in inf['versions']:
                pretty.add_row([inf['name'], version])
        print(pretty)
    else:
        print("There is no active infrastructure")

def show_infrastructure_instances(infrastructure):
    pretty = PrettyTable(["Infrastructure name", "Version", "Instance name", "Instance id", "Status"])
    if len(infrastructure):
        for inf in infrastructure:
            for version in inf['versions']:
                for instance in inf['cloudServers']:
                    pretty.add_row([inf['name'], version, instance['servername'], instance['id'], instance['status']])
        print(pretty)
    else:
        print("There is no active infrastructure")