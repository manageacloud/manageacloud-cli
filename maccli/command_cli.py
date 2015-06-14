import getpass
import ConfigParser
import sys
import time
from os.path import join, expanduser

import service.auth
import service.instance
import service.provider
import service.macfile
import service.infrastructure
import maccli.facade.macfile
import maccli.service.configuration
from view.view_generic import show_error, show
import view.view_location
import view.view_instance
import view.view_cookbook
import view.view_generic
import view.view_infrastructure
import maccli.view.view_hardware
from config import AUTH_SECTION, USER_OPTION, APIKEY_OPTION, MAC_FILE, EXCEPTION_EXIT_CODE
from maccli.helper.exception import MacParseEnvException, MacErrorCreatingTier, MacParseParamException


def help():
    view.view_generic.general_help()


def login():
    try:
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


def instance_ssh(instance_id, command):
    try:
        service.instance.ssh_instance(instance_id, command)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
        show_error(e)
        sys.exit(EXCEPTION_EXIT_CODE)


def instance_create(cookbook_tag, deployment, location, servername, provider, release, branch, hardware, lifespan,
                    environments, hd, port):
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
                    show("There is not locations available for configuration %s and provider %s" % (cookbook_tag, provider))

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
            instance = service.instance.create_instance(cookbook_tag, deployment, location, servername, provider, release,
                                                        branch, hardware, lifespan, environments, hd, port)
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


def instance_ssh_help():
    view.view_instance.show_instance_ssh_help()


def instance_destroy(ids):
    try:
        maccli.logger.debug("Destroying instances %s " % ids)
        instances = []
        for instanceid in ids:
            maccli.logger.debug("Destroying instance %s " % ids)
            instance = service.instance.destroy_instance(instanceid)
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

        root, roles, infrastructures = maccli.service.macfile.parse_macfile(raw)

        if not resume:
            existing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])

            if len(existing_instances) > 0:
                view.view_generic.show()
                view.view_generic.show()
                view.view_generic.show_error(
                    "There are active instances for infrastructure %s and version %s" % (root['name'], root['version']))
                view.view_generic.show()
                view.view_generic.show()
                view.view_instance.show_instances(existing_instances)
                view.view_generic.show()
                view.view_generic.show()
                exit(7)

            if quiet:
                view.view_generic.show("Infrastructure %s version %s" % (root['name'], root['version']))
            else:
                view.view_generic.header("Infrastructure %s version %s" % (root['name'], root['version']), "=")

            roles_created = {}
            try:
                """ Create all the servers """
                for infrastructure_key in infrastructures:
                    infrastructure = infrastructures[infrastructure_key]
                    infrastructure_role = infrastructure['role']
                    if quiet:
                        view.view_generic.show("[%s][%s] Infrastructure tier" % (infrastructure_key, infrastructure['role']))
                    else:
                        view.view_generic.header("[%s][%s] Infrastructure tier" % (infrastructure_key, infrastructure['role']))
                    role_raw = roles[infrastructure_role]["instance create"]
                    metadata = service.instance.metadata(root, infrastructure_key, infrastructure_role, role_raw, infrastructure)
                    instances = maccli.facade.macfile.create_tier(role_raw, infrastructure, metadata, quiet)
                    roles_created[infrastructure_role] = instances

            except MacErrorCreatingTier:
                view.view_generic.show_error("ERROR: An error happened while creating tier. Server failed.")
                view.view_generic.show_error("HINT: Use 'mac instance log <instance id>' for details")
                view.view_generic.show("Task raised errors.")
                exit(5)

            except MacParseEnvException as e:
                view.view_generic.show_error("ERROR: An error happened parsing environments." + str(type(e)) + str(e.args))
                view.view_generic.show("Task raised errors.")
                exit(6)

        finish = False
        while not finish:
            processing_instances = service.instance.list_by_infrastructure(root['name'], root['version'])
            if not quiet:
                view.view_generic.clear()
                view.view_instance.show_instances(processing_instances)
            maccli.facade.macfile.apply_infrastructure_changes(processing_instances, root['name'], root['version'], quiet)
            finish = True
            for instance in processing_instances:
                if not (instance['status'].startswith("Ready") or instance['status'] == "Creation failed" or instance['status'] == "Configuration Error"):
                    finish = False
                if on_failure is not None and (instance['status'] == "Creation failed" or instance['status'] == "Configuration Error"):
                    finish = True

            if not finish:
                time.sleep(3)

        instances_processed = service.instance.list_by_infrastructure(root['name'], root['version'])
        if not quiet:
            view.view_generic.clear()
        view.view_instance.show_instances(instances_processed)

        # Clean up if failure
        failed = maccli.facade.macfile.clean_up(instances_processed, on_failure)

        if failed:
            view.view_generic.show("Infrastructure failed.")
            exit(12)
        else:
            view.view_generic.show("Infrastructure created successfully.")
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
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
        view.view_infrastructure.show_infrastructure_instances(infrastructure)
    except KeyboardInterrupt:
        show_error("Aborting")
    except Exception as e:
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
