import getpass
import ConfigParser
import logging
import os
import sys
import time
from os.path import join, expanduser
import traceback
import threading
from urllib2 import URLError
import urllib2
import urlparse

import service.auth
import service.instance
import service.provider
import service.macfile
import service.resource
import service.infrastructure
import maccli.facade.macfile
import maccli.service.configuration
import maccli.helper.macfile
import maccli.helper.cmd
from view.view_generic import show_error, show
import view.view_location
import view.view_instance
import view.view_cookbook
import view.view_generic
import view.view_resource
import view.view_infrastructure
import maccli.view.view_hardware
from view.view_generic import GREEN, RED
from config import AUTH_SECTION, USER_OPTION, APIKEY_OPTION, MAC_FILE, EXCEPTION_EXIT_CODE, CONFIGURATION_FAILED, \
    CREATION_FAILED
from maccli.helper.exception import MacParseEnvException, MacErrorCreatingTier, MacParseParamException, \
    MacResourceException, MacJsonException


def help():
    view.view_generic.general_help()


def login():
    try:
        view.view_generic.show("")
        view.view_generic.show("If you are using Manageacloud SaaS and you don't have credentials, please register at https://manageacloud.com")
        view.view_generic.show("")
        view.view_generic.show("If you are using Manageacloud Community please set the following variable:")
        view.view_generic.show("    export MAC=http://my_community_server/api/v1/")
        view.view_generic.show("")
        view.view_generic.show("More information at http://manageacloud/docs/getting-started/install")
        view.view_generic.show("")
        username = raw_input("Username or email: ")
        password = getpass.getpass()

        user, api_key = service.auth.authenticate(username, password)
        if api_key is not None:
            config = ConfigParser.ConfigParser()
            config.add_section(AUTH_SECTION)
            config.set(AUTH_SECTION, USER_OPTION, user)
            config.set(AUTH_SECTION, APIKEY_OPTION, api_key)
            with open(join(expanduser('~'), MAC_FILE), 'w') as cfgfile:
                config.write(cfgfile)
            print("Login succeeded!")

    except KeyboardInterrupt as e:
        show_error("")
        show_error("Authentication cancelled.")

    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def no_credentials():
    show("You need to login into Manageacloud.com")
    show()
    show("    mac login")
    show()
    show("If you do not have an account, register at https://manageacloud.com/register")


def instance_list():
    try:
        json = service.instance.list_instances()
        view.view_instance.show_instances(json)

    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_ssh(raw_ids, command):

    if raw_ids == ["all"]:  # run in all instances
        ids = service.instance.list_instances()
    else:
        ids = service.instance.list_instances(name_or_ids=raw_ids)

    try:
        # array for job list
        jobs = []

        for id in ids:
            if command is None:
                service.instance.ssh_interactive_instance(id['id'])
            else:
                # define and add job
                t = threading.Thread(target=_run_cmd_simple,args=(id["servername"], id["id"], command))
                jobs.append(t)

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def _run_cmd_simple(server_name, raw_id, command):
    rc, stdout, stderr = service.instance.ssh_command_instance(raw_id, command)
    maccli.view.view_generic.showc("[%s]" % server_name, GREEN)
    if stdout:
        maccli.view.view_generic.show(stdout)
    if stderr:
        maccli.view.view_generic.showc(stderr, RED)
    maccli.view.view_generic.show()


def instance_create(cookbook_tag, bootstrap_raw, deployment, location, servername, provider, release_raw, release_version_raw,
                    branch, hardware, lifespan, environments, hd, port, net):

    # allow format release:release_version, ie ubuntu:trusty
    if ":" in release_raw:
        release, release_version = release_raw.split(":", 1)
    else:
        release = release_raw
        release_version = release_version_raw


    # TODO check if cookbook_tag exists
    # TODO validate bootstrap inputs
    try:
        if cookbook_tag is None and bootstrap_raw is None:
            view.view_instance.show_instance_create_help()

        elif location is None:
            locations_json = service.provider.list_locations(provider, release)
            if locations_json is not None:
                show()
                show("--location parameter not set. You must choose the location.")
                show()
                show("Available locations:")
                show()
                if len(locations_json):
                    view.view_location.show_locations(locations_json)
                    view.view_instance.show_create_example_with_parameters(cookbook_tag, bootstrap_raw, deployment,
                                                                           locations_json[0]['id'], servername,
                                                                           provider, release, release_version,
                                                                           branch, hardware)

                else:
                    type = None
                    if release is not None:
                        type = release

                    if type is None and cookbook_tag is not None:
                        type = cookbook_tag

                    show("There is not locations available for '%s' and provider '%s'" % (type, provider))

                view.view_instance.show_instance_help()

        elif deployment == "production" and hardware is None or \
                                        deployment == "testing" and provider is not "default" and hardware is None:
            hardwares = service.provider.list_hardwares(provider, location, release)
            show()
            show("--hardware not found. You must choose the hardware.")
            show()
            show("Available hardware:")
            show()
            view.view_hardware.show_hardwares(hardwares)
            if (len(hardwares) > 0):
                view.view_instance.show_create_example_with_parameters(cookbook_tag, bootstrap_raw, deployment, location, servername,
                                                                       provider, release, release_version, branch, hardwares[0]['id'])
        else:
            """ Execute create instance """

            # load the bootstrap file properly
            if bootstrap_raw is not None:
                if os.path.exists(bootstrap_raw):  # it is a file
                    # this is going to be the PWD to run commands
                    maccli.pwd = os.path.dirname(os.path.realpath(bootstrap_raw))
                    maccli.logger.info("Path %s exists, trying to open file", bootstrap_raw)
                    stream = open(bootstrap_raw, "r")
                    bootstrap = stream.read()
                elif _is_url(bootstrap_raw):  # try url
                    maccli.logger.info("%s looks like an URL, trying to open URL" % bootstrap_raw)
                    f = urllib2.urlopen(bootstrap_raw)
                    bootstrap = f.read()
                else:  # values are bash executable
                    bootstrap = bootstrap_raw
            else:
                bootstrap = bootstrap_raw

            if cookbook_tag == "" and bootstrap == "":
                show_error("Server contains no configuration")
            else:
                instance = service.instance.create_instance(cookbook_tag, bootstrap, deployment, location,
                                                            servername, provider, release, release_version,
                                                            branch, hardware, lifespan, environments, hd, port, net)
                if instance is not None:
                    view.view_instance.show_instance(instance)

                view.view_generic.show("")
                view.view_generic.show("Monitor the progress of all servers:")
                view.view_generic.show("")
                view.view_generic.show("    watch mac instance list")
                view.view_generic.show("")
                view.view_generic.show("Tail server logs:")
                view.view_generic.show("")
                view.view_generic.show("    mac instance log -f %s" % instance['id'])
                view.view_generic.show("")
    except KeyboardInterrupt:
        show_error("Aborting")
    except URLError:
        show_error("Can't open URL %s" % bootstrap_raw)
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def _is_url(url):
    return bool(urlparse.urlparse(url).scheme)


def instance_destroy_help():
    view.view_instance.show_instance_destroy_help()


def instance_update_help():
    view.view_instance.show_instance_update_help()


def instance_ssh_help():
    view.view_instance.show_instance_ssh_help()


def instance_destroy(ids):
    try:
        maccli.logger.debug("Destroying instances %s " % ids)
        instances = []
        for instance_id in ids:
            maccli.logger.debug("Destroying instance %s " % instance_id)
            instance = service.instance.destroy_instance(instance_id)
            instances.append(instance)

        if instances is not None:
            view.view_instance.show_instances(instances)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_update(raw_ids, cookbook_tag, bootstrap):
    try:
        if raw_ids == ["all"]:  # run in all instances
            ids = service.instance.list_instances()
        else:
            ids = service.instance.list_instances(name_or_ids=raw_ids)

        instances = []
        for id in ids:
            maccli.logger.debug("Updating instance %s " % id['id'])
            instance = service.instance.update_configuration(cookbook_tag, bootstrap, id['id'])
            instances.append(instance)

        if instances is not None:
            view.view_instance.show_instances(instances)

        view.view_generic.show("")
        view.view_generic.show("To track configuration changes")
        view.view_generic.show("")
        for id in ids:
            view.view_generic.show("    mac instance log -f %s" % id['id'])

        view.view_generic.show("")

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def provider_help():
    view.view_generic.show_provider_help()


def credentials(provider, clientid, key_raw, force_file):
    """
    Save the credential's supplier if are correct.

    :param provider:
    :param clientid:
    :param key_raw: This might be a path. If so, the credentials are stored in the file.
    :return:
    """
    try:
        service.provider.save_credentials(provider, clientid, key_raw, force_file)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def resouce_get_stdout(infrastructure_name, infrastructure_version, resource_name, key):

    try:
        output = service.resource.get_resource_value(infrastructure_name, infrastructure_version, resource_name, key)
        if isinstance(output,basestring):
            sys.stdout.write(output)
        else:
            print(output)

    except KeyError:
        show_error("Key '%s' not found" % key)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_help():
    view.view_instance.show_instance_help()


def configuration_list():
    try:
        configurations = service.configuration.list_configurations()
        view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_search(keywords, show_url):
    try:
        configurations = service.configuration.search_configurations(keywords)
        if show_url:
            view.view_cookbook.show_configurations_url(configurations)
        else:
            view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_help():
    view.view_cookbook.show_configurations_help()


def convert_to_yaml(args):
    yaml = service.macfile.convert_args_to_yaml(args)
    view.view_generic.show(yaml)


def process_macfile(file, resume, params, quiet, on_failure):
    try:
        # save the PWD
        maccli.helper.cmd.update_pwd(file)

        raw = maccli.helper.macfile.load_macfile(file)
        try:
            raw = maccli.service.macfile.parse_params(raw, params)
        except MacParseParamException, e:
            view.view_generic.show_error(e.message)
            exit(11)

        root, roles, infrastructures, actions, resources = (None,) * 5
        try:
            root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(raw)
        except MacParseParamException, e:
            view.view_generic.show_error(e.message)
            exit(12)

        if not resume:

            existing_infrastructures = service.infrastructure.search_instances(root['name'], root['version'])

            if len(existing_infrastructures) > 0:
                view.view_generic.show()
                view.view_generic.show()
                view.view_generic.show_error(
                    "There are active instances for infrastructure '%s' and version '%s'" % (root['name'], root['version']))
                view.view_generic.show()
                view.view_generic.show()
                view.view_infrastructure.show_infrastructure_instances(existing_infrastructures)
                view.view_infrastructure.show_resources_in_infrastructure(existing_infrastructures)
                view.view_generic.show()
                view.view_generic.show()
                view.view_generic.show(
                    "Instances and resources must be destroyed before attempting to create another "
                    "infrastructure using the same version.")
                view.view_generic.show("")
                view.view_generic.show("To destroy the complete infrastructure:")
                view.view_generic.show("    mac infrastructure destroy <infrastructure name> <infrastructure version>")
                view.view_generic.show("")
                view.view_generic.show("To view the infrastructure available:")
                view.view_generic.show("    mac infrastructure list")
                view.view_generic.show("")
                view.view_generic.show("To view the resources and instances in a infrastructure:")
                view.view_generic.show("    mac infrastructure items")
                view.view_generic.show("")


                exit(7)

            if quiet:
                view.view_generic.show("Infrastructure %s version %s" % (root['name'], root['version']))
            else:
                view.view_generic.header("Infrastructure %s version %s" % (root['name'], root['version']), "=")

        infrastructure_error_detail = None
        finish = False
        infrastructure_resources_failed = False
        infrastructure_resources_processed = []  # looks for the non-instance infrastructure
        processing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])
        while not finish:
            if not quiet:
                view.view_generic.clear()
                view.view_instance.show_instances(processing_instances)
                view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)

            # apply configuration to the instances
            maccli.facade.macfile.apply_instance_infrastructure_changes(processing_instances, root['name'], root['version'], quiet, infrastructures, infrastructure_resources_processed)

            # process resources
            finish = True
            try:
                processed_resources_part, finish_resources = maccli.facade.macfile.apply_resources(processing_instances, infrastructure_resources_processed, processing_instances, roles, infrastructures, actions, resources, root, quiet)
                maccli.logger.debug("Resources processed this run: %s " % processed_resources_part)
                infrastructure_resources_processed = infrastructure_resources_processed + processed_resources_part
                maccli.logger.debug("Total resources processed: %s " % infrastructure_resources_processed)
                finish = finish and finish_resources
            except MacResourceException as e:
                infrastructure_error_detail = e[1]
                infrastructure_resources_failed = True
                finish = True

            # check instances has been processed
            processing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])
            for instance in processing_instances:
                if not (instance['status'].startswith("Ready") or instance['status'] == CREATION_FAILED or instance['status'] == CONFIGURATION_FAILED):
                    finish = False
                if on_failure is not None and (instance['status'] == CREATION_FAILED or instance['status'] == CONFIGURATION_FAILED):
                    finish = finish and True

            if infrastructure_resources_failed:
                finish = True
            else:
                if not finish:
                    time.sleep(3)

        instances_processed = service.instance.list_by_infrastructure(root['name'], root['version'])
        if not quiet:
            view.view_generic.clear()
        view.view_instance.show_instances(instances_processed)
        view.view_infrastructure.show_infrastructure_resources(infrastructures, infrastructure_resources_processed)
        view.view_generic.show("")
        view.view_resource.show_resources(infrastructure_resources_processed)

        # Clean up if failure
        instances_failed = maccli.facade.macfile.clean_up(instances_processed, on_failure)

        if instances_failed or infrastructure_resources_failed:
            view.view_generic.show("")
            view.view_generic.showc("Infrastructure failed.", RED)

            # Of the error is in infrastructure, display it.
            if infrastructure_error_detail is not None:
                view.view_generic.show("")
                if 'stderr' in infrastructure_error_detail:
                    view.view_generic.show(infrastructure_error_detail['stderr'])
                else:
                    view.view_generic.show(infrastructure_error_detail)

                if 'cmd' in infrastructure_error_detail:
                    view.view_generic.show(infrastructure_error_detail['cmd'])

            # if an instance failed, the details of the error are in the log
            view.view_generic.show("")
            view.view_generic.show("Logs available at")
            view.view_generic.show("    mac instance log <instance id or name>")
            exit(12)
        else:
            view.view_generic.showc("Infrastructure created successfully.", GREEN)
            view.view_generic.show("")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            traceback.print_exc(file=sys.stdout)
        else:
            show_error(e)

        sys.exit(EXCEPTION_EXIT_CODE)


def instance_fact(instance_id):
    try:
        json = service.instance.facts(instance_id)
        view.view_instance.show_facts(json)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_log(instance_id, follow):
    try:
        if follow:
            while True:
                logs = maccli.service.instance.log(instance_id, follow)
                if logs == "":
                    time.sleep(5)
                else:
                    view.view_generic.show(logs)
                    time.sleep(1)
        else:
            json = service.instance.log(instance_id, False)
            view.view_instance.show_logs(json)

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_lifespan(instance_id, amount):
    try:
        instance = service.instance.lifespan(instance_id, amount)
        view.view_instance.show_instance(instance)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_list():
    try:
        infrastructure = service.infrastructure.list_infrastructure()
        view.view_infrastructure.show_infrastructure(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_search(name, version):
    try:
        infrastructure = service.infrastructure.search_instances(name, version)
        if len(infrastructure):
            view.view_infrastructure.show_infrastructure_instances(infrastructure)
            view.view_generic.show()
            view.view_infrastructure.show_resources_in_infrastructure(infrastructure)
        else:
            view.view_generic.show("There are not active infrastructure")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_update(name, version, cookbook_tag):
    try:
        infrastructures = service.infrastructure.search_instances(name, version)

        if len(infrastructures):
            infrastructure = infrastructures[0]

            instances = []
            for instance in infrastructure['cloudServers']:
                instance_updated = service.instance.update_configuration(cookbook_tag, "", instance['id'])
                instances.append(instance_updated)

            if instances is not None:
                view.view_instance.show_instances(instances)
        else:
            maccli.view.view_generic.show("Infrastructure '%s' version '%s' not found" % (name, version))

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            traceback.print_exc(file=sys.stdout)
        else:
            show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_destroy(name, version):
    try:
        infrastructures = service.infrastructure.search_instances(name, version)

        if len(infrastructures):
            infrastructure = infrastructures[0]

            for instance in infrastructure['cloudServers']:
                maccli.view.view_generic.showc("Instance %s marked as deleted" % instance['id'], GREEN)
                maccli.view.view_generic.show("")
                maccli.service.instance.destroy_instance(instance['id'])

            if len(infrastructure['cloudServers']):
                time.sleep(5)  # give some time to instances to free resources

            for resource in infrastructure['resources']:
                try:
                    maccli.facade.macfile.destroy_resource(resource, infrastructure['cloudServers'], infrastructure['resources'])
                except MacJsonException as e:
                    maccli.view.view_generic.showc("\nError while destroying resource %s\n\n" % resource['name'], RED)
                    maccli.view.view_generic.showc("Error while navigating json! %s\n" % e.message, RED)

        else:
            maccli.view.view_generic.show("Infrastructure '%s' version '%s' not found" % (name, version))

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            traceback.print_exc(file=sys.stdout)
        else:
            show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_lifespan(amount, name, version):
    try:
        infrastructure = service.infrastructure.lifespan(amount, name, version)
        view.view_infrastructure.show_infrastructure_instances(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_ssh_keys(name, version, known_host):
    """
    Diplays ssh keys or adds it to known_hosts

    :param name:
    :param version:
    :param known_host:
    :return:
    """
    try:
        ssh_keys = service.infrastructure.keys(name, version, known_host)
        if not maccli.quiet:
            if known_host:
                for ssh_key in ssh_keys:
                    show("%s processed" % ssh_key['cloudServer']['ipv4'])

            else:
                for ssh_key in ssh_keys:
                    show(ssh_key['stdout'])

    except KeyboardInterrupt:
       show_error("Aborting")
    except Exception as e:
       show_error(e)
       sys.exit(EXCEPTION_EXIT_CODE)
