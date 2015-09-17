import getpass
import ConfigParser
import logging
import sys
import time
from os.path import join, expanduser
import traceback

import service.auth
import service.instance
import service.provider
import service.macfile
import service.resource
import service.infrastructure
import maccli.facade.macfile
import maccli.service.configuration
import maccli.helper.macfile
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
    MacResourceException


def help():
    view.view_generic.general_help()


def login():
    try:
        view.view_generic.show("")
        view.view_generic.show("If you don't have credentials, please register at https://manageacloud.com")
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
    show("If you do not have an account, you can register one at https://manageacloud.com/register")


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
        for id in ids:
            if command is None:
                service.instance.ssh_interactive_instance(id['id'])
            else:
                maccli.view.view_generic.showc("[%s]" % id['servername'], GREEN)
                rc, stdout, stderr = service.instance.ssh_command_instance(id['id'], command)
                if stdout:
                    maccli.view.view_generic.show(stdout)
                if stderr:
                    maccli.view.view_generic.showc(stderr, RED)
                maccli.view.view_generic.show()

    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_create(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port, net):
    try:
        if cookbook_tag is None:
            view.view_instance.show_instance_create_help()

        elif location is None:
            locations_json = service.provider.list_locations(cookbook_tag, provider, release)
            if locations_json is not None:
                show()
                show("--location parameter not set. You must choose the location.")
                show()
                show("Available locations:")
                show()
                if len(locations_json):
                    view.view_location.show_locations(locations_json)
                    view.view_instance.show_create_example_with_parameters(cookbook_tag, deployment,
                                                                           locations_json[0]['id'], servername,
                                                                           provider, release, branch, hardware)

                else:
                    show("There is not locations available for configuration %s and provider %s" % (
                        cookbook_tag, provider))

                view.view_instance.show_instance_help()
        elif deployment == "production" and hardware is None or \
                                        deployment == "testing" and provider is not "manageacloud" and hardware is None:
            hardwares = service.provider.list_hardwares(provider, location, cookbook_tag, release)
            show()
            show("--hardware not found. You must choose the hardware.")
            show()
            show("Available hardware:")
            show()
            view.view_hardware.show_hardwares(hardwares)
            if (len(hardwares) > 0):
                view.view_instance.show_create_example_with_parameters(cookbook_tag, deployment, location, servername,
                                                                       provider, release, branch, hardwares[0]['id'])
        else:
            """ Execute create instance """
            instance = service.instance.create_instance(cookbook_tag, deployment, location, servername, provider,
                                                        release,
                                                        branch, hardware, lifespan, environments, hd, port, net)
            if instance is not None:
                view.view_instance.show_instance(instance)

            view.view_generic.show("")
            view.view_generic.show("To monitor the creation progress:")
            view.view_generic.show("")
            view.view_generic.show("watch mac instance list")
            view.view_generic.show("")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


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


def instance_update(raw_ids):
    try:
        if raw_ids == ["all"]:  # run in all instances
            ids = service.instance.list_instances()
        else:
            ids = service.instance.list_instances(name_or_ids=raw_ids)

        instances = []
        for id in ids:
            maccli.logger.debug("Updating instance %s " % id['id'])
            instance = service.instance.update_configuration("", id['id'])
            instances.append(instance)

        if instances is not None:
            view.view_instance.show_instances(instances)
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

        raw = maccli.service.macfile.load_macfile(file)
        try:
            raw = maccli.service.macfile.parse_params(raw, params)
        except MacParseParamException, e:
            view.view_generic.show_error(e.message)
            exit(11)

        root, roles, infrastructures, actions, resources = maccli.service.macfile.parse_macfile(raw)

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
                    "Instances must be destroyed before attempting to create another "
                    "infrastructure using the same version.")
                view.view_generic.show("")
                view.view_generic.show("To destroy instances:")
                view.view_generic.show("    mac instance destroy <instance id or name>")
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


def instance_log(instance_id):
    try:
        json = service.instance.log(instance_id)
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
                maccli.facade.macfile.destroy_resource(resource, infrastructure['cloudServers'], infrastructure['resources'])
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
