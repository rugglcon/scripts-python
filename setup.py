#!/usr/bin/python

"""
this script is a python version
of the original shell setup script
for my scripts repo
"""

import sys
import os
import errno

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

def check_dir(dir):
    full_path = os.path.abspath(dir)
    if os.path.isdir(full_path):
        return 1
    else:
        return 0

def mkdir_p(dir):
    full_path = os.path.abspath(dir)
    try:
        os.makedirs(full_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(full_path):
            pass
        else:
            raise

def path_check():
    if bindir not in path:
        if check_dir(bindir):
            print "adding", bindir, "to PATH..."
            with open(home + "/.profile", "a") as profile:
                profile.write("\nexport PATH=" + path + ":" + bindir)
        else:
            make_dir(bindir)
    else:
        print bindir, "already exists in PATH"

def get_args(arg_list):
    if len(arg_list) > 0:
        if "-h" in arg_list:
            usage()
            sys.exit(1)
        elif "-b" in arg_list:
            bpos = arg_list.index("-b")
            set_dir = arg_list[bpos + 1]
            if check_dir(set_dir):
                global bindir
                bindir = set_dir
                path_check()
                return 1
            else:
                make_dir(set_dir)
        else:
            error_trig("Invalid argument: " + arg_list[0] + ". Run with -h for help.")


# def install(path):

def main():
    get_args(sys.argv[1:])
    print bindir

main()
