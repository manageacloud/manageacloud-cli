from __future__ import print_function
import sys


def show(string=""):
    print(string)


def show_error(string):
    print(string, file=sys.stderr)

def clear():
    print(chr(27) + "[2J")

def general_help():
    print("Welcome to the Pre-alpha version of Manageacloud.cli. This tool is under heavy development.")
    print("For more information, please visit https://alpha.manageacloud.com")
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