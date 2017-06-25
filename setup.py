#!/usr/bin/python

""" this script is a python version
of the original shell setup script
for my scripts repo """

import sys
import os
import string

home = os.path.expanduser('~')
bindir = home + "/bin"
path_add = 1
path = os.environ['PATH']

def error_trig(message):
    print "&s\n" % message
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
    bin_set = 0
    for arg in arg_list:


def main():
    get_args(sys.argv)

main()
# print sys.argv
