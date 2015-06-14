from __future__ import print_function
import sys


def show(string=""):
    print(string)


def show_error(string):
    print(string, file=sys.stderr)


def clear():
    print(chr(27) + "[2J")


def general_help():
    print("Welcome to the beta version of Manageacloud cli.")
    print("For more information, please visit https://manageacloud.com")
    print("")
    print("To display the available options:")
    print("")
    print("    mac -h")
    print("")


def header(text, char=None):
    if char is None:
        char = "-"
    print(text)
    print(char * len(text))
    print()