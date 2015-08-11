from __future__ import print_function
import sys

# define colors
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def show(string=""):
    print(string)


def showc(string, colour=WHITE):
    if _has_colours(sys.stdout):
        seq = "\x1b[1;%dm" % (30 + colour) + string + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(string)


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


def cmd_error(command, rc, stdout, stderr):
    show_error("Script exited with code %s" % rc)
    show_error(command)
    show_error("Error details: %s" % stderr)
    if stdout != "":
        show_error("Extra output: %s " % stdout)


def _has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        import curses

        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


