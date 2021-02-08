from collections import OrderedDict
from maccli.helper.exception import MacParseParamException
from maccli.helper.unsortable import ordered_load, yaml
import maccli.helper.macfile


def resolve_inheritance(macfile_str, params):
    """
    Loads the macfile and solves the inheritance
    """
    params_found = []
    raw, found = maccli.helper.macfile.parse_params(macfile_str, params)
    params_found += found
    raw = ordered_load(raw, yaml.SafeLoader)

    if 'parents' in raw:  # there is inheritance

        # load the parents. For now, only one level of inheritance is allowed
        parents_raw = {}
        for parent in raw['parents']:
            parent_raw = maccli.helper.macfile.load_macfile(raw['parents'][parent])
            parent_raw, found = maccli.helper.macfile.parse_params(parent_raw, params)
            params_found += found
            parents_raw[parent] = ordered_load(parent_raw, yaml.SafeLoader)

        # lets read the original file and paste all the information from the parent class
        if 'actions' not in raw:
            raw['actions'] = {}  # order is not important here

        if 'resources' not in raw:
            raw['resources'] = {}  # order is not important here

        # add 'resources' and 'actions' from parents
        for key in parents_raw:
            parent_raw = parents_raw[key]

            if 'actions' in parent_raw:
                for action in parent_raw['actions']:
                    if action in raw['actions']:
                        maccli.logger.info("Action %s exists, it wont be overwritten by %s.%s", action, key, action)
                    else:
                        raw['actions'][action] = parent_raw['actions'][action]

            if 'resources' in parent_raw:
                for resource in parent_raw['resources']:
                    if resource in raw['resources']:
                        maccli.logger.info("Resource %s exists, it wont be overwritten by %s.%s", resource, key, resource)
                    else:
                        raw['resources'][resource] = parent_raw['resources'][resource]


        """
            To fix the infrastructure section, we have to reconstruct it by using the "defaults" from the parent
            Format:
              # Overwriting a section
              # single case
              aws.image_base_inf:
                name: app
                provider: amazon
                location: us-east-1
                hardware: t1.micro
                role: app
                release: ubuntu
                amount: 1

               # Appending a single section using the defaults
               # single case
               aws.image_base_inf:

               # Appending all the sections that has not been defined already, using the defaults
               # wildcard case
               aws.*
        """

        if 'infrastructures' in raw:

            clean_infrastructures = OrderedDict({})
            for key in raw['infrastructures']:
                raw_values = raw['infrastructures'][key]
                if raw_values is None:
                    raw_values = {}

                if key[-2:] == '.*':
                    # wildcard case
                    parent, section = key.split(".")
                    default_infrastructures = parents_raw[parent]['defaults']
                    for default_infrastructure_key in default_infrastructures:
                        default_infrastructure_values = default_infrastructures[default_infrastructure_key]
                        if not (default_infrastructure_key in raw['infrastructures'] or parent + '.' + default_infrastructure_key in raw['infrastructures']):
                            maccli.logger.debug("Inheritance wildcard adds to infrastructure %s", default_infrastructure_key)
                            clean_infrastructures.update({default_infrastructure_key: default_infrastructure_values})

                elif '.' in key:
                    # single case
                    parent, section = key.split(".")
                    default_values = parents_raw[parent]['defaults'][section]

                    if default_values is not None:
                        for default_key in default_values:
                            default_value = default_values[default_key]
                            if default_key not in raw_values:  # add the key
                                raw_values[default_key] = default_value
                            else:  # merge the key
                                raw_values[default_key] = _merge_dictionaries(default_value, raw_values[default_key])

                    maccli.logger.debug("Inheritance single adds to infrastructure %s", section)
                    clean_infrastructures.update({section: raw_values})
                else:
                    # no inheritance work
                    maccli.logger.debug("Inheritance adds to infrastructure %s", key)
                    clean_infrastructures.update({key: raw_values})

            maccli.logger.debug("Inheritance defines clean infrastructure %s", clean_infrastructures)
            raw['infrastructures'] = clean_infrastructures

        if len(set(params_found)) != len(set(params)):
            # remove found parameters
            missing_parameters = [x for x in params if x.split("=")[0] not in params_found]
            raise MacParseParamException("Variable(s) %s could not be found in macfile" % missing_parameters)

        # remove the parents
        del raw['parents']

    return raw


def _merge_dictionaries(base, new_values):
    if isinstance(new_values, str):
        total = new_values
    else:
        total = base
        for key in new_values:
            value = new_values[key]
            total[key] = value

    return total