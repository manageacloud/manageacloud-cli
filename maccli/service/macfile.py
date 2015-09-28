from __future__ import print_function
from collections import OrderedDict
import os

import yaml
import yaml.representer
import re

from maccli.view.view_generic import show_error
from maccli.helper.exception import MacParamValidationError, MacParseParamException
from maccli.helper.unsortable import ordered_load
import maccli
from maccli.helper.unsortable import UnsortableOrderedDict


""" Yaml file format
description: Manageacloud CLI
version: 0.1a6
timestamp: '2015-02-05 11:59:07'
roles:
  default:
    instance create:
      branch: master
      configuration: basic_ubuntu_1404
      deployment: testing
      environment:
      - DBNAME: pgbench
      - PGUSER: benchuser
      hardware: https://www.googleapis.com/compute/v1/projects/soy-sound-613/zones/asia-east1-a/machineTypes/f1-micro
      location: asia-east1-a
      name: localtesting
      provider: gce
      release: any
"""


def convert_args_to_yaml(args):
    maccli.logger.debug("Converting options %s: " % args)
    key = ""
    if args.cmd is not None and args.subcmd is not None:
        key = args.cmd + ' ' + args.subcmd
    elif args.cmd is not None:
        key = args.cmd

    attributes = filter(
        lambda a: not a.startswith('_') and a not in ["cmd", "subcmd", "yaml", "debug", "verbose", "quiet"], dir(args))

    # defines the parameter that must exist, even if empty
    empty_parameters = ['name']

    params_instance = UnsortableOrderedDict()
    params_infrastructure = UnsortableOrderedDict()
    for attr in attributes:
        if attr in empty_parameters:
            value = ""
        else:
            value = getattr(args, attr)

        if value is not None:
            if attr in ['hardware', 'location', 'provider', 'deployment', 'lifespan', 'name', 'release']:
                params_infrastructure[attr] = value
            else:
                params_instance[attr] = value

    # default roles, what tier can be created
    params_role = UnsortableOrderedDict()
    params_role[key] = params_instance
    role_name = "default"
    roles = UnsortableOrderedDict()
    roles["default"] = params_role

    # default infrastructures, create one
    params_infrastructure['role'] = role_name
    params_infrastructure['amount'] = 1
    infrastructures = UnsortableOrderedDict()
    infrastructures["default"] = params_infrastructure

    # general structure
    data = UnsortableOrderedDict()
    data["mac"] = maccli.__version__
    data["description"] = "Manageacloud CLI"
    data["name"] = "manageacloud.com"
    data["version"] = "1.0"
    data["roles"] = roles
    data["infrastructures"] = infrastructures

    yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
    return yaml.dump(data, default_flow_style=False)


def validate_param(actual, expected, optional=None):
    unexpected = is_unexpected(actual, expected)
    if optional is not None:
        unexpected_optional = is_unexpected(unexpected, optional)
    else:
        unexpected_optional = unexpected

    if len(unexpected_optional):
        error = "Incorrect file format. The following parameters are unexpected:\n"
        for p in unexpected_optional:
            error += " - %s\n" % p
        raise MacParamValidationError(error)

    notpresent = is_present(actual, expected)
    if optional is not None:
        notpresent_optional = is_unexpected(notpresent, optional)
    else:
        notpresent_optional = notpresent

    if len(notpresent_optional):
        error = "Incorrect file format. The following parameters are needed and not present:\n"
        for p in notpresent_optional:
            error += " - %s\n" % p
        raise MacParamValidationError(error)


def is_present(actual, expected):
    """ evaluates if all params in actual exist in expected  """
    if expected is None:
        notfound = actual
    else:
        notfound = filter(lambda x: x not in actual, expected)
    return notfound


def is_unexpected(actual, expected):
    """ evaluates if there is a parameter in actual that does not exist in expected  """
    if expected is None:
        unexpected = actual
    else:
        unexpected = filter(lambda x: x not in expected, actual)
    return unexpected


def parse_params(raw, params_raw):
    """
    The content of macfiles might have parameters to parse.
    """

    clean = raw
    if params_raw is not None:
        for param in params_raw:
            key, value = param.split("=", 1)
            clean_tmp = clean.replace("{%s}" % key, value)
            if clean == clean_tmp:
                raise MacParseParamException("Variable %s cloud not be found in macfile" % key)
            clean = clean_tmp

    if re.search(r'{([a-zA-Z_\-]*?)}', clean, re.MULTILINE):
        raise MacParseParamException("MACFILE contains parameters that were not available:\n"
                                     "\n"
                                     "%s"
                                     "\n"
                                     "Available parameters %s" % (clean, str(params_raw)))
    return clean


def load_macfile(path):

    # this is going to be the PWD to run commands
    maccli.pwd = os.path.dirname(os.path.realpath(path))

    # open file
    stream = open(path, "r")

    return stream.read()


def parse_macfile(string):
    raw = ordered_load(string, yaml.SafeLoader)

    """

    Parse and validates the macfile and returns structured contents

    :param raw: R
    :return: root, role and infrastructure contents
    """
    # validate root
    root_params = ['mac', 'version', 'name', 'description', 'infrastructures']
    root_params_optional = ['actions', 'resources', 'roles']
    raw_root_keys = raw.keys()
    try:
        validate_param(raw_root_keys, root_params, root_params_optional)
    except MacParamValidationError, e:
        show_error(e.message)
        exit(1)

    # validate roles
    expected_roles = []
    role_root_params = ["instance create"]
    role_params = ['configuration']
    role_optional_params = ['branch', 'hd', 'lifespan', 'environment']

    if 'roles' in raw:
        if raw['roles'] is None:
            show_error("Roles section defined but empty")
            exit(1)
        else:
            raw_role_root_keys = raw['roles'].keys()
            for key_role_root in raw_role_root_keys:
                expected_roles.append(key_role_root)
                raw_role_keys = raw['roles'][key_role_root].keys()
                try:
                    validate_param(raw_role_keys, role_root_params)
                    for key_role in raw_role_keys:
                        raw_role = raw['roles'][key_role_root][key_role].keys()
                        validate_param(raw_role, role_params, role_optional_params)
                except MacParamValidationError, e:
                    show_error(e.message)
                    exit(1)
    else:
        raw['roles'] = []

    # validate infrastructures
    raw_infrastructure_root_keys = raw['infrastructures'].keys()
    actual_roles = []
    for key_infrastructure_root in raw_infrastructure_root_keys:
        raw_infrastructure_keys = raw['infrastructures'][key_infrastructure_root].keys()
        if 'role' in raw_infrastructure_keys:
            """ Infrastructure related with a role """
            infrastructure_optional_params = ['lifespan', 'deployment', 'release', 'provider', 'hardware', 'amount',
                                              'environment', 'ready', 'net']
            infrastructure_root_params = ['amount', 'role', 'hardware', 'location', 'provider', 'name', 'deployment',
                                          'release']
            infrastructure_root_params_mac = ['amount', 'role', 'location', 'provider', 'name', 'deployment',
                                              'release']

            try:
                provider = raw['infrastructures'][key_infrastructure_root]['provider']
            except:
                provider = ""

            try:
                if provider == "manageacloud":
                    validate_param(raw_infrastructure_keys, infrastructure_root_params_mac, infrastructure_optional_params)
                else:
                    validate_param(raw_infrastructure_keys, infrastructure_root_params, infrastructure_optional_params)
            except MacParamValidationError, e:
                show_error(e.message)
                exit(1)

            actual_roles.append(raw['infrastructures'][key_infrastructure_root]["role"])
        else:
            """ Infrastructure related with a resource"""
            infrastructure_optional_params = ['resource', 'action', 'ready', 'params']
            validate_param(raw_infrastructure_keys, None, infrastructure_optional_params)

    # validate actions
    if 'actions' in raw.keys():
        actions_optional_params = ["ssh", "bash"]
        raw_actions_root_keys = raw['actions'].keys()
        for key_action_root in raw_actions_root_keys:
            if isinstance(raw['actions'][key_action_root], OrderedDict):
                raw_action_keys = raw['actions'][key_action_root].keys()
                if len(raw_action_keys) != 1:
                    print("The action '%s' does not have anything defined." % key_action_root)
                    exit(1)
                validate_param(raw_action_keys, None, actions_optional_params)
            else:
                print("The action '%s' has wrong format." % key_action_root)
                exit(1)

    else:
        raw['actions'] = []

    # validate resources
    if 'resources' in raw.keys():
        resources_optional_params = ["create bash", "destroy bash"]
        raw_resources_root_keys = raw['resources'].keys()
        for key_resource_root in raw_resources_root_keys:
            if isinstance(raw['resources'][key_resource_root], OrderedDict):
                raw_resource_keys = raw['resources'][key_resource_root].keys()
                if len(raw_resource_keys) < 1:
                    print("The resource '%s' does not have anything defined." % key_resource_root)
                    exit(1)
                validate_param(raw_resource_keys, None, resources_optional_params)
            else:
                print("The resource '%s' has wrong format." % key_resource_root)
                exit(1)

    else:
        raw['resources'] = []

    # check the values of infrastructures > default > role
    not_existing_roles = is_unexpected(actual_roles, expected_roles)
    if len(not_existing_roles):
        print("The following roles are used under 'infrastructures' but are never defined:")
        for p in not_existing_roles:
            print(" - %s" % p)
        exit(3)

    # check the values of infrastructures > default > role
    not_existing_roles = is_present(actual_roles, expected_roles)
    if len(not_existing_roles):
        print("WARNING! The following roles are defined but never user:")
        for p in not_existing_roles:
            print(" - %s" % p)

    # get the root parameters
    root = {
        'version': raw['version'],
        'name': raw['name'],
    }

    return root, raw['roles'], raw['infrastructures'], raw['actions'], raw['resources']