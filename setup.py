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
    while True:
        feedback = raw_input(dir + " doesn't exist, create it? [Y/n] ")
        if feedback == 'Y' or feedback == 'y':
            try:
                os.makedirs(full_path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(full_path):
                    pass
                else:
                    raise

            return
        elif feedback == 'N' or feedback == 'n':
            error_trig("Please make destination or change it and try again.")
        else:
            print "Please enter Y(y) or n(N)"

def path_check(set_dir):
    if set_dir not in path:
        if check_dir(set_dir):
            print "adding", set_dir, "to PATH..."
            with open(home + "/.profile", "a") as profile:
                profile.write("\nexport PATH=" + path + ":" + set_dir)
        else:
            mkdir_p(set_dir)
    else:
        print set_dir, "already exists in PATH"

def get_args(arg_list):
    set_dir = bindir
    if len(arg_list) > 0:
        if "-h" in arg_list:
            usage()
            sys.exit(1)
        elif "-b" in arg_list:
            bpos = arg_list.index("-b")
            if len(arg_list) > bpos:
                set_dir = arg_list[bpos + 1]
            else:
                error_trig("no path specified after '-b' option. Run with -h for help.")

        else:
            error_trig("Invalid argument: " + arg_list[0] + ". Run with -h for help.")

    path_check(set_dir)


# def install(path):

def main():
    get_args(sys.argv[1:])
    print bindir

main()
