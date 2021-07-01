import getpass
import configparser
import logging
import os
import sys
import time
from os.path import join, expanduser
import traceback
import threading
import urllib
import urllib.request
import urllib.parse

# TODO implement progress bar
#from progressbar import ReverseBar, Percentage, ETA, RotatingMarker, Timer, ProgressBar

import maccli.service.auth
import maccli.service.instance
import maccli.service.provider
import maccli.service.macfile
import maccli.service.resource
import maccli.service.infrastructure
import maccli.facade.macfile
import maccli.service.configuration
import maccli.helper.macfile
import maccli.helper.cmd
import maccli.dao.inheritance
from maccli.view.view_generic import show_error, show
import maccli.view.view_location
import maccli.view.view_instance
import maccli.view.view_cookbook
import maccli.view.view_generic
import maccli.view.view_resource
import maccli.view.view_infrastructure
import maccli.view.view_hardware
from maccli.view.view_generic import GREEN, RED
from maccli.config import AUTH_SECTION, USER_OPTION, APIKEY_OPTION, MAC_FILE, EXCEPTION_EXIT_CODE, CONFIGURATION_FAILED, \
    CREATION_FAILED
from maccli.helper.exception import MacParseEnvException, MacErrorCreatingTier, MacParseParamException, \
    MacResourceException, MacJsonException


def help():
    maccli.view.view_generic.general_help()


def login():
    try:
        maccli.view.view_generic.show("")
        maccli.view.view_generic.show(
            "If you are using Manageacloud SaaS and you don't have credentials, please register at https://manageacloud.com")
        maccli.view.view_generic.show("")
        maccli.view.view_generic.show("If you are using Manageacloud Community please set the following variable:")
        maccli.view.view_generic.show("    export MAC=http://my_community_server/api/v1/")
        maccli.view.view_generic.show("")
        maccli.view.view_generic.show("More information at http://manageacloud/docs/getting-started/install")
        maccli.view.view_generic.show("")
        username = input("Username or email: ")
        password = getpass.getpass()

        user, api_key = maccli.service.auth.authenticate(username, password)
        if api_key is not None:
            config = configparser.ConfigParser()
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
    # try:
    json = maccli.service.instance.list_instances()
    maccli.view.view_instance.show_instances(json)

    # except Exception as e:
    #     show_error(e)
    #     sys.exit(EXCEPTION_EXIT_CODE)


def instance_ssh(raw_ids, command):
    # TODO move to parameter
    active_job_limit = 50

    if raw_ids == ["all"]:  # run in all instances
        ids = maccli.service.instance.list_instances()
    else:
        ids = maccli.service.instance.list_instances(name_or_ids=raw_ids)

    try:
        # array for job list
        jobs = {}

        maccli.logger.debug("Starting threads for command %s" % command)

        started_count = 0
        completed_count = 0
        total_count = len(ids)

        # bar = ProgressBar(maxval=total_count,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()

        for id in ids:
            server_name = id["servername"]
            raw_id = id["id"]
            if command is None:
                maccli.service.instance.ssh_interactive_instance(id['id'])
            else:
                # define and add job
                t = threading.Thread(target=_run_cmd_simple, args=(server_name, raw_id, command))

                maccli.logger.debug("Starting job for %s. Active Jobs: %s." % (server_name, len(jobs)))
                if not t.is_alive():
                    started_count += 1
                    t.start()

                jobs[raw_id] = t

                # check if we are above the limit
                need_to_sleep = True
                while len(jobs) >= active_job_limit:
                    maccli.logger.debug("Job limit reached. Active Jobs: %s." % len(jobs))

                    keys = list(jobs.keys())
                    for key in keys:
                        if not jobs[key].is_alive():
                            completed_count += 1
                            # bar.update(completed_count)
                            show("Status: %s/%s/%s" % (completed_count, started_count, total_count))
                            jobs[key].join()
                            del jobs[key]
                            need_to_sleep = False
                        maccli.logger.debug("Job finished. Active Jobs: %s." % len(jobs))

                    if need_to_sleep:
                        time.sleep(1)

        # waiting for the existing thread to finish.
        # if a thread is too slow, we will report it
        slow_threads = {}
        while len(jobs) > 0:

            keys = list(jobs.keys())
            for key in keys:

                if not jobs[key].is_alive():
                    completed_count += 1
                    # bar.update(completed_count)
                    show("Status: %s/%s/%s" % (completed_count, started_count, total_count))
                    jobs[key].join()
                    del jobs[key]
                    if key in slow_threads:
                        del slow_threads[key]
                else:
                    if key in slow_threads:
                        if slow_threads[key] > 10:
                            show("Server %s is running the query slow: %s secs" % (key, slow_threads[key]))
                        slow_threads[key] += 1
                    else:
                        slow_threads[key] = 1

            time.sleep(1)

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        tb = traceback.format_exc()
        show_error(e)
        show_error(tb)
        sys.exit(EXCEPTION_EXIT_CODE)


def _run_cmd_simple(server_name, raw_id, command):
    rc, stdout, stderr = maccli.service.instance.ssh_command_instance(raw_id, command)
    maccli.view.view_generic.showc("[%s] " % server_name, GREEN)
    if stdout:
        maccli.view.view_generic.show(stdout)
    elif stderr:
        maccli.view.view_generic.showc(raw_id, RED)
        maccli.view.view_generic.showc(stderr, RED)
    else:
        maccli.view.view_generic.show("\n")
    #maccli.view.view_generic.show()


def instance_create(cookbook_tag, bootstrap_raw, deployment, location, servername, provider, release_raw,
                    release_version_raw,
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
            maccli.view.view_instance.show_instance_create_help()

        elif location is None:
            locations_json = maccli.service.provider.list_locations(provider, release)
            if locations_json is not None:
                show()
                show("--location parameter not set. You must choose the location.")
                show()
                show("Available locations:")
                show()
                if len(locations_json):
                    maccli.view.view_location.show_locations(locations_json)
                    maccli.view.view_instance.show_create_example_with_parameters(cookbook_tag, bootstrap_raw,
                                                                                  deployment,
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

                maccli.view.view_instance.show_instance_help()

        elif deployment == "production" and hardware is None or \
                deployment == "testing" and provider != "default" and hardware is None:
            hardwares = maccli.service.provider.list_hardwares(provider, location, release)
            show()
            show("--hardware not found. You must choose the hardware.")
            show()
            show("Available hardware:")
            show()
            maccli.view.view_hardware.show_hardwares(hardwares)
            if (len(hardwares) > 0):
                maccli.view.view_instance.show_create_example_with_parameters(cookbook_tag, bootstrap_raw, deployment,
                                                                              location, servername,
                                                                              provider, release, release_version,
                                                                              branch, hardwares[0]['id'])
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
                    f = urllib.request.urlopen(bootstrap_raw)
                    bootstrap = f.read()
                else:  # values are bash executable
                    bootstrap = bootstrap_raw
            else:
                bootstrap = bootstrap_raw

            if cookbook_tag == "" and bootstrap == "":
                show_error("Server contains no configuration")
            else:
                instance = maccli.service.instance.create_instance(cookbook_tag, bootstrap, deployment, location,
                                                                   servername, provider, release, release_version,
                                                                   branch, hardware, lifespan, environments, hd, port,
                                                                   net)
                if instance is not None:
                    maccli.view.view_instance.show_instance(instance)

                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("Monitor the progress of all servers:")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("    watch mac instance list")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("Tail server logs:")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("    mac instance log -f %s" % instance['id'])
                maccli.view.view_generic.show("")
    except KeyboardInterrupt:
        show_error("Aborting")
    # except URLError:
    #     show_error("Can't open URL %s" % bootstrap_raw)
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def _is_url(url):
    return bool(urllib.parse.urlparse(url).scheme)


def instance_destroy_help():
    maccli.view.view_instance.show_instance_destroy_help()


def instance_update_help():
    maccli.view.view_instance.show_instance_update_help()


def instance_ssh_help():
    maccli.view.view_instance.show_instance_ssh_help()


def instance_destroy(ids):
    try:
        maccli.logger.debug("Destroying instances %s " % ids)
        instances = []
        for instance_id in ids:
            maccli.logger.debug("Destroying instance %s " % instance_id)
            instance = maccli.service.instance.destroy_instance(instance_id)
            instances.append(instance)

        if instances is not None:
            maccli.view.view_instance.show_instances(instances)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_update(raw_ids, cookbook_tag, bootstrap):
    try:
        if raw_ids == ["all"]:  # run in all instances
            ids = maccli.service.instance.list_instances()
        else:
            ids = maccli.service.instance.list_instances(name_or_ids=raw_ids)

        instances = []
        for id in ids:
            maccli.logger.debug("Updating instance %s " % id['id'])
            instance = maccli.service.instance.update_configuration(cookbook_tag, bootstrap, id['id'])
            instances.append(instance)

        if instances is not None:
            maccli.view.view_instance.show_instances(instances)

        maccli.view.view_generic.show("")
        maccli.view.view_generic.show("To track configuration changes")
        maccli.view.view_generic.show("")
        for id in ids:
            maccli.view.view_generic.show("    mac instance log -f %s" % id['id'])

        maccli.view.view_generic.show("")

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def provider_help():
    maccli.view.view_generic.show_provider_help()


def credentials(provider, clientid, key_raw, force_file):
    """
    Save the credential's supplier if are correct.

    :param provider:
    :param clientid:
    :param key_raw: This might be a path. If so, the credentials are stored in the file.
    :return:
    """
    try:
        maccli.service.provider.save_credentials(provider, clientid, key_raw, force_file)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def resouce_get_stdout(infrastructure_name, infrastructure_version, resource_name, key):
    try:
        output = maccli.service.resource.get_resource_value(infrastructure_name, infrastructure_version, resource_name,
                                                            key)
        if isinstance(output, str):
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
    maccli.view.view_instance.show_instance_help()


def configuration_list():
    try:
        configurations = maccli.service.configuration.list_configurations()
        maccli.view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_search(keywords, show_url):
    try:
        configurations = maccli.service.configuration.search_configurations(keywords)
        if show_url:
            maccli.view.view_cookbook.show_configurations_url(configurations)
        else:
            maccli.view.view_cookbook.show_configurations(configurations)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def configuration_help():
    maccli.view.view_cookbook.show_configurations_help()


def convert_to_yaml(args):
    yaml = maccli.service.macfile.convert_args_to_yaml(args)
    maccli.view.view_generic.show(yaml)


def process_macfile(file, resume, params, quiet, on_failure):
    try:
        # save the PWD
        maccli.helper.cmd.update_pwd(file)

        raw = maccli.helper.macfile.load_macfile(file)

        macfile_raw = None
        try:
            macfile_raw = maccli.dao.inheritance.resolve_inheritance(raw, params)
        except MacParseParamException as e:
            maccli.view.view_generic.show_error(e)
            exit(11)

        root, roles, infrastructures, actions, resources = (None,) * 5
        try:
            root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(macfile_raw)
        except MacParseParamException as e:
            maccli.view.view_generic.show_error(e)
            exit(12)

        if not resume:

            existing_infrastructures = maccli.service.infrastructure.search_instances(root['name'], root['version'])

            if len(existing_infrastructures) > 0:
                maccli.view.view_generic.show()
                maccli.view.view_generic.show()
                maccli.view.view_generic.show_error(
                    "There are active instances for infrastructure '%s' and version '%s'" % (
                    root['name'], root['version']))
                maccli.view.view_generic.show()
                maccli.view.view_generic.show()
                maccli.view.view_infrastructure.show_infrastructure_instances(existing_infrastructures)
                maccli.view.view_infrastructure.show_resources_in_infrastructure(existing_infrastructures)
                maccli.view.view_generic.show()
                maccli.view.view_generic.show()
                maccli.view.view_generic.show(
                    "Instances and resources must be destroyed before attempting to create another "
                    "infrastructure using the same version.")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("To destroy the complete infrastructure:")
                maccli.view.view_generic.show(
                    "    mac infrastructure destroy <infrastructure name> <infrastructure version>")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("To view the infrastructure available:")
                maccli.view.view_generic.show("    mac infrastructure list")
                maccli.view.view_generic.show("")
                maccli.view.view_generic.show("To view the resources and instances in a infrastructure:")
                maccli.view.view_generic.show("    mac infrastructure items")
                maccli.view.view_generic.show("")

                exit(7)

            if quiet:
                maccli.view.view_generic.show("Infrastructure %s version %s" % (root['name'], root['version']))
            else:
                maccli.view.view_generic.header("Infrastructure %s version %s" % (root['name'], root['version']), "=")

        infrastructure_error_detail = None
        finish = False
        infrastructure_resources_failed = False
        infrastructure_resources_processed = []  # looks for the non-instance infrastructure
        processing_instances = maccli.service.instance.list_by_infrastructure(root['name'], root['version'])
        while not finish:
            if not quiet:
                maccli.view.view_generic.clear()
                maccli.view.view_instance.show_instances(processing_instances)
                maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures,
                                                                              infrastructure_resources_processed)

            # apply configuration to the instances
            maccli.facade.macfile.apply_instance_infrastructure_changes(processing_instances, root['name'],
                                                                        root['version'], quiet, infrastructures,
                                                                        infrastructure_resources_processed)

            # process resources
            finish = True
            try:
                processed_resources_part, finish_resources = maccli.facade.macfile.apply_resources(processing_instances,
                                                                                                   infrastructure_resources_processed,
                                                                                                   processing_instances,
                                                                                                   roles,
                                                                                                   infrastructures,
                                                                                                   actions, resources,
                                                                                                   root, quiet)
                maccli.logger.debug("Resources processed this run: %s " % processed_resources_part)
                infrastructure_resources_processed = infrastructure_resources_processed + processed_resources_part
                maccli.logger.debug("Total resources processed: %s " % infrastructure_resources_processed)
                finish = finish and finish_resources
            except MacResourceException as e:
                infrastructure_error_detail = [e.__str__()]
                infrastructure_resources_failed = True
                finish = True

            # check instances has been processed
            processing_instances = maccli.service.instance.list_by_infrastructure(root['name'], root['version'])
            for instance in processing_instances:
                if not (instance['status'].startswith("Ready") or instance['status'] == CREATION_FAILED or instance[
                    'status'] == CONFIGURATION_FAILED):
                    finish = False
                if on_failure is not None and (
                        instance['status'] == CREATION_FAILED or instance['status'] == CONFIGURATION_FAILED):
                    finish = finish and True

            if infrastructure_resources_failed:
                finish = True
            else:
                if not finish:
                    time.sleep(3)

        instances_processed = maccli.service.instance.list_by_infrastructure(root['name'], root['version'])
        if not quiet:
            maccli.view.view_generic.clear()
        maccli.view.view_instance.show_instances(instances_processed)
        maccli.view.view_infrastructure.show_infrastructure_resources(infrastructures,
                                                                      infrastructure_resources_processed)
        maccli.view.view_generic.show("")
        maccli.view.view_resource.show_resources(infrastructure_resources_processed)

        # Clean up if failure
        instances_failed = maccli.facade.macfile.clean_up(instances_processed, on_failure)

        if instances_failed or infrastructure_resources_failed:
            maccli.view.view_generic.show("")
            maccli.view.view_generic.showc("Infrastructure failed.", RED)

            # Of the error is in infrastructure, display it.
            if infrastructure_error_detail is not None:
                maccli.view.view_generic.show("")
                if 'stderr' in infrastructure_error_detail:
                    maccli.view.view_generic.show(infrastructure_error_detail['stderr'])
                else:
                    maccli.view.view_generic.show(infrastructure_error_detail)

                if 'cmd' in infrastructure_error_detail:
                    maccli.view.view_generic.show(infrastructure_error_detail['cmd'])

            # if an instance failed, the details of the error are in the log
            maccli.view.view_generic.show("")
            maccli.view.view_generic.show("Logs available at")
            maccli.view.view_generic.show("    mac instance log <instance id or name>")
            exit(12)
        else:
            maccli.view.view_generic.showc("Infrastructure created successfully.", GREEN)
            maccli.view.view_generic.show("")
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
        json = maccli.service.instance.facts(instance_id)
        maccli.view.view_instance.show_facts(json)
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
                    maccli.view.view_generic.show(logs)
                    time.sleep(1)
        else:
            json = maccli.service.instance.log(instance_id, False)
            maccli.view.view_instance.show_logs(json)

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_lifespan(instance_id, amount):
    try:
        instance = maccli.service.instance.lifespan(instance_id, amount)
        maccli.view.view_instance.show_instance(instance)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_list():
    try:
        infrastructure = maccli.service.infrastructure.list_infrastructure()
        maccli.view.view_infrastructure.show_infrastructure(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_search(name, version):
    try:
        infrastructure = maccli.service.infrastructure.search_instances(name, version)
        if len(infrastructure):
            maccli.view.view_infrastructure.show_infrastructure_instances(infrastructure)
            maccli.view.view_generic.show()
            maccli.view.view_infrastructure.show_resources_in_infrastructure(infrastructure)
        else:
            maccli.view.view_generic.show("There are not active infrastructure")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def infrastructure_update(name, version, cookbook_tag):
    try:
        infrastructures = maccli.service.infrastructure.search_instances(name, version)

        if len(infrastructures):
            infrastructure = infrastructures[0]

            instances = []
            for instance in infrastructure['cloudServers']:
                instance_updated = maccli.service.instance.update_configuration(cookbook_tag, "", instance['id'])
                instances.append(instance_updated)

            if instances is not None:
                maccli.view.view_instance.show_instances(instances)
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
        infrastructures = maccli.service.infrastructure.search_instances(name, version)

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
                    maccli.facade.macfile.destroy_resource(resource, infrastructure['cloudServers'],
                                                           infrastructure['resources'])
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
        infrastructure = maccli.service.infrastructure.lifespan(amount, name, version)
        maccli.view.view_infrastructure.show_infrastructure_instances(infrastructure)
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
        ssh_keys = maccli.service.infrastructure.keys(name, version, known_host)
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
