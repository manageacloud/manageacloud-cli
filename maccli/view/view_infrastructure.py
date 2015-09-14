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
    is_output = False
    for inf in infrastructure:
        for version in inf['versions']:
            for instance in inf['cloudServers']:
                instance_infrastructure_version = instance['metadata']['infrastructure']['version']
                if version == instance_infrastructure_version:
                    if instance['type'] == 'testing' and instance['status'] == "Ready":
                        status = "%s (%im left)" % (instance['status'], instance['lifespan'])
                    else:
                        status = instance['status']
                    pretty.add_row([inf['name'], version, instance['servername'], instance['id'], status])
                    is_output = True
    if is_output:
        print(pretty)
    else:
        print("There is no active instances in infrastructure")


def show_resources_in_infrastructure(infrastructures):

    """  Display resources in infrastrucrures """
    if len(infrastructures):
        pretty = PrettyTable(["Infrastructure name", "Version", "Resource type", "Resource name", "Status"])
        pretty.align = "l"

        is_output = False
        for inf in infrastructures:
            for version in inf['versions']:
                for resource in inf['resources']:
                    resource_type = resource['metadata']['infrastructure']['macfile_resource_name']
                    resource_name = resource['metadata']['infrastructure']['macfile_infrastructure_name']
                    resource_version = resource['metadata']['infrastructure']['version']
                    if version == resource_version:
                        status = ""
                        if 'destroy' in resource:
                            if resource['create']['rc']:
                                status = "Destroy failed"
                            else:
                                status = "Destroyed"

                        elif 'create' in resource:
                            if resource['create']['rc']:
                                status = "Creation failed"
                            else:
                                status = "Ready"

                        pretty.add_row([inf['name'], version, resource_type, resource_name, status])
                        is_output = True

        if is_output:
            print(pretty)
        else:
            print("There is no resources in infrastructure")


def show_infrastructure_resources(infrastructures, infrastructures_resources_processed):
    """ display table with infrastructure when it is being processed """

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
