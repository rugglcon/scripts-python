#!/usr/bin/env python

"""
this script is a python version
of the original shell setup script
for my scripts repo
"""

from sys import argv
import os
import errno
from shutil import copy, copystat, rmtree

# declare useful globals
HOME = os.path.expanduser('~')

BINDIR = HOME + "/bin"

CONFDIR = HOME

PATHADD = 1

PATH = os.environ['PATH']

# start functions
def error_trig(message):
    """
    error_trig

    @param message: the message to be output
    @returns: nothing
    """
    print "Error:", message
    exit(1)

def usage():
    """
    prints help
    """
    print "Usage: ./setup.py [OPTIONS]"
    print "Examples: ./setup.py -b", BINDIR
    print "          ./setup.py"
    print "Options:"
    print "-b /path/to/bin    Install dir. Default is", BINDIR
    print "-h                 Print this help."

def check_dir(dir_to_check):
    """
    check_dir

    @param dir_to_check: explains itself
    @return: 1 if the full path to 'dir_to_check' is a dir, 0 otherwise
    """
    full_path = os.path.abspath(dir_to_check)
    if os.path.isdir(full_path):
        return 1
    else:
        return 0

def mkdir_p(dir_to_check):
    """
    mkdir_p
    provides functionality of mkdir -p

    @param dir_to_check: the directory to check and see if we should make it or not
    @return: 0 if any errors occurred while making directory, 1 if directory is made without error,
    and exits if it was chosen not to make the directory
    """
    full_path = os.path.abspath(dir_to_check)
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return 1

    while True:
        feedback = raw_input(dir_to_check + " doesn't exist, create it? [Y/n] ")
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
    """
    path_check
    checks if BINDIR is in your $PATH

    @param set_dir: directory to search for in PATH
    @return: nothing, just prints useful messages to the console
    """
    set_dir = os.path.abspath(set_dir)
    if set_dir not in PATH:
        if mkdir_p(set_dir):
            print "adding", set_dir, "to PATH..."
            with open(HOME + "/.profile", "a+") as profile:
                profile.write("export PATH=\"" + PATH + ":" + set_dir + "\"")

            print "For the scripts to be readily available, you must source '$HOME/.profile'."
        else:
            error_trig("Something went wrong while making directory.")
    else:
        print set_dir, "already exists in PATH"

    global BINDIR
    BINDIR = set_dir

def get_args(arg_list):
    """
    get_args

    @param arg_list: list of arguments to the script
    @return: nothing, just prints messages if necessary
    """
    set_dir = BINDIR
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
    """
    force_symlink
    tries to force to make a symbolic link from source to dest

    @param source: hard copy of file/directory
    @param dest: destination of link
    """
    try:
        os.symlink(source, dest)
    except OSError, exc:
        if exc.errno == errno.EEXIST:
            if os.path.isdir(dest):
                rmtree(dest)
            else:
                os.remove(dest)
            os.symlink(source, dest)

def install_scripts():
    """
    installs the scripts
    """
    print "installing scripts..."

    all_scripts = os.listdir("./scripts")
    os.chdir("scripts")
    for script in all_scripts:
        copy(script, BINDIR)
        copystat(script, BINDIR)

def install_configs():
    """
    installs the config files
    """
    print "linking configs..."
    force_symlink(os.path.abspath(".vim"), CONFDIR + "/.vim")
    force_symlink(os.path.abspath("cava"), CONFDIR + "/.config/cava")
    force_symlink(os.path.abspath(".bash_aliases"), CONFDIR + "/.bash_aliases")
    force_symlink(os.path.abspath(".bashrc"), CONFDIR + "/.bashrc")
    force_symlink(os.path.abspath(".profile"), CONFDIR + "/.profile")
    force_symlink(os.path.abspath(".tmux.conf"), CONFDIR + "/.tmux.conf")
    force_symlink(os.path.abspath(".xinitrc"), CONFDIR + "/.xinitrc")

def main():
    """
    main function
    """
    get_args(argv[1:])

    # passed all the checks, go ahead and install scripts
    install_scripts()
    install_configs()

    print "done."

main()
