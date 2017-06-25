#!/usr/bin/python

"""
this script is a python version
of the original shell setup script
for my scripts repo
"""

import sys
import os
import string

global home, bindir, path_add, path
home = os.path.expanduser('~')
bindir = home + "/bin"
path_add = 1
path = os.environ['PATH']

def error_trig(message):
    print "Error:", message
    sys.exit(1)

def usage():
    print "Usage: ./setup.py [OPTIONS]"
    print "Examples: ./setup.py -b", bindir
    print "          ./setup.py"
    print "Options:"
    print "-b /path/to/bin    Install dir. Default is", bindir
    print "-h                 Print this help."

def path_check():
    if bindir not in path:
        print "adding", bindir, "to PATH..."
        with open(home + "/.profile", "a") as profile:
            profile.write("\nexport PATH=" + path + ":" + bindir)
    else:
        print bindir, "already exists in PATH"

def get_args(arg_list):
    global bindir
    if len(arg_list) > 0:
        if "-h" in arg_list:
            usage()
            sys.exit(1)
        elif "-b" in arg_list:
            bpos = arg_list.index("-b")
            set_dir = arg_list[bpos + 1]
        else:
            error_trig("Invalid argument: " + arg_list[0] + ". Run with -h for help.")

# def install(path):

def main():
    global bindir
    get_args(sys.argv[1:])
    print bindir

main()
