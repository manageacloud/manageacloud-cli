from __future__ import print_function
from prettytable import PrettyTable


def show_hardwares(hardwares):
    pretty = PrettyTable(["Id", "RAM", "Cores", "HD"])
    pretty.align = "r"
    pretty.align["Id"] = "l"
    for hardware in hardwares:
        processor_clean = ""
        for processor in hardware['processors']:
            if processor_clean != "":
                processor_clean += "\n"
            processor_clean += ("%s" % processor['cores'])

        volume_clean = ""
        for volume in hardware['volumes']:
            if volume_clean != "":
                volume_clean += "\n"

            volume_clean += ("%sGb" % volume['size'])

        pretty.add_row([hardware['id'], hardware['ram'], processor_clean, volume_clean])

    print(pretty)
