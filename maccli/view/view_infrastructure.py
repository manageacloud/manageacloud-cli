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
                    if instance['type'] == 'testing' and instance['status'] == "Ready":
                        status = "%s (%im left)" % (instance['status'], instance['lifespan'])
                    else:
                        status = instance['status']

                    pretty.add_row([inf['name'], version, instance['servername'], instance['id'], status])
        print(pretty)
    else:
        print("There is no active infrastructure")


def show_infrastructure_resources(infrastructures, infrastructures_resources_processed):

    if len(infrastructures):
        pretty = PrettyTable(["Resource name", "Status"])
        pretty.align = "l"

        print_table = False
        for infrastructure in infrastructures.items():
            print_table = True
            resource_name = infrastructure[0]
            status = "Pending"
            for resource_processed in infrastructures_resources_processed:
                key = resource_processed.iterkeys().next()
                if key == resource_name:
                    rp = resource_processed[key]
                    rc = rp['rc']
                    stderr = rp['stderr']
                    if rc != 0:
                        status = "Failed"
                    else:
                        if not (stderr == '' or stderr is None):
                            status = "OK, but stderr not empty"
                        else:
                            status = "OK"

            pretty.add_row([resource_name, status])

        if print_table:
            print(pretty)
