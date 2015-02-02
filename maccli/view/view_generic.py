from __future__ import print_function
import sys


def show(string=""):
    print(string)


def show_error(string):
    print(string, file=sys.stderr)


def general_help():
    print("Welcome to the Pre-alpha version of Manageacloud.cli. This tool is under heavy development.")
    print("For more information, please visit https://alpha.manageacloud.com")
    print("")
    print("To display the available options:")
    print("")
    print("    mac -h")
    print("")