#!/usr/bin/env python

"""
this script is a python version
of the original shell setup script
for my scripts repo
"""

from sys import exit, argv
import os
import errno
from shutil import copy, copystat, rmtree

# declare useful globals
global home
home = os.path.expanduser('~')

global bindir
bindir = home + "/bin"

global confdir
confdir = home

global path_add
path_add = 1

global path
path = os.environ['PATH']

# start functions
def error_trig(message):
    print "Error:", message
    exit(1)

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
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return 1

    while True:
        feedback = raw_input(dir + " doesn't exist, create it? [Y/n] ")
        if feedback == 'Y' or feedback == 'y':
            try:
                os.makedirs(full_path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(full_path):
                    pass
                else:
                    print "Error occurred:", exc.errno
                    return 0

            return 1
        elif feedback == 'N' or feedback == 'n':
            error_trig("Please make destination or change it and try again.")
        else:
            print "Please enter Y(y) or n(N)"

def path_check(set_dir):
    set_dir = os.path.abspath(set_dir)
    if set_dir not in path:
        if mkdir_p(set_dir):
            print "adding", set_dir, "to PATH..."
            with open(home + "/.profile", "a+") as profile:
                profile.write("export PATH=\"" + path + ":" + set_dir + "\"")

            print "In order for the scripts to be readily available, you must source '$HOME/.profile'."
        else:
            error_trig("Something went wrong while making directory.")
    else:
        print set_dir, "already exists in PATH"

    global bindir
    bindir = set_dir

def get_args(arg_list):
    set_dir = bindir
    if len(arg_list) > 0:
        if "-h" in arg_list:
            usage()
            exit(1)
        elif "-b" in arg_list:
            bpos = arg_list.index("-b")
            if len(arg_list) > bpos:
                set_dir = arg_list[bpos + 1]
            else:
                error_trig("no path specified after '-b' option. Run with -h for help.")

        else:
            error_trig("Invalid argument: " + arg_list[0] + ". Run with -h for help.")

    path_check(set_dir)

def force_symlink(source, dest):
    try:
        os.symlink(source, dest)
    except OSError, e:
        if e.errno == errno.EEXIST:
            if os.isdir(dest):
                rmtree(dest)
            else:
                os.remove(dest)
            os.symlink(source, dest)

def install_scripts():
    print "installing scripts..."
    
    all_scripts = os.listdir("./scripts")
    os.chdir("scripts")
    for script in all_scripts:
        copy(script, bindir)
        copystat(script, bindir)

def install_configs():
    print "linking configs..."
    force_symlink(os.abspath(".vim"), confdir + "/.vim")
    force_symlink(os.abspath("cava"), confdir + "/.config/cava")
    force_symlink(os.abspath(".bash_aliases"), confdir + "/.bash_aliases")
    force_symlink(os.abspath(".bashrc"), confdir + "/.bashrc")
    force_symlink(os.abspath(".profile"), confdir + "/.profile")
    force_symlink(os.abspath(".tmux.conf"), confdir + "/.tmux.conf")
    force_symlink(os.abspath(".xinitrc"), confdir + "/.xinitrc")

def main():
    get_args(argv[1:])
    
    # passed all the checks, go ahead and install scripts
    install_scripts()

    print "done."

main()
