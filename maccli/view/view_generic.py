from __future__ import print_function
import sys


def show(string=""):
    print(string)


def show_error(string):
    print(string, file=sys.stderr)


def general_help():
    print("")
    print("To display the available options:")
    print("")
    print("    mac -h")
    print("")