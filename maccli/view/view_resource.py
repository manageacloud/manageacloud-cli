from __future__ import print_function

import maccli.view.view_generic
from prettytable import PrettyTable


def show_resources(resources):

    if len(resources):
        for resource in resources:
            for key in resource.keys():
                r = resource[key]
                maccli.view.view_generic.header("Resource %s" % key, "-")
                if r['rc']:
                    maccli.view.view_generic.show("Process failed. Return code: %s. Output:" % r['rc'])
                    maccli.view.view_generic.show(r['stderr'])
                    if r['stdout'] is not None and r['stdout'].strip():
                        maccli.view.view_generic.show("Standard output not empty:")
                        maccli.view.view_generic.show(r['stdout'])
                else:
                    maccli.view.view_generic.show("Execution successful. Output:")
                    maccli.view.view_generic.show(r['stdout'])
                    if r['stderr'] is not None and r['stderr'].strip():
                        maccli.view.view_generic.show("Standard error not empty:")
                        maccli.view.view_generic.show(r['stderr'])

    else:
        print("There are no resources available")

