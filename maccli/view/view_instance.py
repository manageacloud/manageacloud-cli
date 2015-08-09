from __future__ import print_function
import sys

from prettytable import PrettyTable
import maccli.view.view_generic


def show_instances(instances):
    pretty = PrettyTable(["Instance name", "IP", "Instance ID", "Type", "Status"])

    if len(instances):
        for instance in instances:
            if instance['type'] == 'testing' and instance['status'] == "Ready":
                status = "%s (%im left)" % (instance['status'], instance['lifespan'])
            else:
                status = instance['status']
            pretty.add_row([instance['servername'], instance['ipv4'], instance['id'], instance['type'], status])
        print(pretty)
    else:
        print("There is no active instances")


def show_instance(instance):
    pretty = PrettyTable(["Instance name", "IP", "Instance ID", "Type", "Status"])
    if instance['type'] == 'testing' and instance['status'] == "Ready":
        status = "%s (%im left)" % (instance['status'], instance['lifespan'])
    else:
        status = instance['status']

    pretty.add_row([instance['servername'], instance['ipv4'], instance['id'], instance['type'], status])
    print(pretty)


def show_instance_create_locations_example(cookbook_tag, locationid):
    print("")
    print("Example:")
    print("")
    print("    mac instance create -c %s -l %s" % (cookbook_tag, locationid))
    print("")


def show_instance_create_help():
    print("--configuration parameter is required. ")
    print("")
    print("You can list your configurations:")
    print("")
    print("    mac configuration list")
    print("")
    print("or search public configurations")
    print("")
    print("    mac configuration search")
    print("")
    print("To create a new instance with this configuration:")
    print("")
    print("    mac instance create -c <configuration tag>")
    show_instance_help()


def show_instance_help():
    print("")
    print("Show more help:")
    print("")
    print("    mac instance -h")
    print("")


def show_instance_destroy_help():
    print("")
    print("Show more help:")
    print("")
    print("    mac instance destroy -h")
    print("")


def show_instance_update_help():
    print("")
    print("Show more help:")
    print("")
    print("    mac instance update -h")
    print("")

def show_instance_ssh_help():
    print("")
    print("Show more help:")
    print("")
    print("    mac ssh -h")
    print("")


def show_create_example_with_parameters(cookbook_tag, deployment, location, servername, provider, release, branch,
                                        hardware):
    output = "mac instance create "

    if cookbook_tag is not None and cookbook_tag != "":
        output += " -c " + cookbook_tag

    if deployment is not None and deployment != "testing":
        output += " -d " + deployment

    if location is not None and location != "":
        output += " -l " + location

    if servername is not None and servername != "":
        output += " -n " + servername

    if provider is not None and provider != "manageacloud":
        output += " -p " + provider

    if release is not None and release != "any":
        output += " -r " + release

    if branch is not None and branch != "master":
        output += " -r " + branch

    if hardware is not None and hardware != "":
        output += " -hw " + hardware

    print("")
    print("Example:")
    print("")
    print("    %s" % output)
    print("")


def show_facts(facts):
    for key, value in facts.iteritems():
        print("%s: %s" % (key, value))


def show_logs(logs):
    print("")
    print("")
    if len(logs['cloudServerLogs']) > 0:
        for log in logs['cloudServerLogs']:
            maccli.view.view_generic.header("Creation logs for %s" % log['created'])
            print(log['text'])
    else:
        print("There is not creation logs")

    print("")
    print("")
    if len(logs['cloudServerBlockLogs']) > 0:
        for log in logs['cloudServerBlockLogs']:
            maccli.view.view_generic.header("Configuration logs for %s" % log['created'])
            print(log['text'])
    else:
        print("There is not configuration logs")


def show_processing_instances(instances):
    instances_statuses = {}
    for instance in instances:

        if instance['status'] not in instances_statuses:
            instances_statuses[instance['status']] = 1
        else:
            instances_statuses[instance['status']] = instances_statuses[instance['status']] + 1

    sys.stdout.write("\033[K")
    sys.stdout.write("Progress: ")
    for key in instances_statuses:
        sys.stdout.write("%s: %s " % (key, instances_statuses[key]))
    sys.stdout.write(" \r")
    sys.stdout.flush()