#!/usr/bin/python3
"""
this script is a wrapper for using
rsync, and simplifies it down to use
the options that are commonly used
by me.
"""

from sys import argv
import os
import errno

SYNC_OPTS = "-urpq"

ERR_FILE = "backup_errs.log"

SRC = ""

DEST = ""

def error_trig(message):
    """
    triggers error message and exits
    """
    print("Error:", message)
    exit(1)

def usage():
    """
    prints usage
    """
    print("Usage: backup.py [OPTIONS]")
    print("Examples:         backup.py -e err_file.txt -v")
    print("                  backup")
    print("Options:")
    print("-s, --src /src/dir            Source directory.")
    print("-d, --dest /dest/dir          Destination directory.")
    print("-h, --help                    Print this help.")
    print("-e, --err_file err_file.txt   Output errors to the provided file.")
    print("-v, --verbose                 Turns on verbose logging.")

def check_dirs():
    """
    checks if SRC and DEST are directorys
    """
    full_src = os.path.abspath(SRC)
    full_dest = os.path.abspath(DEST)
    if os.path.isdir(full_src) or os.path.isfile(full_src):
        if not os.path.exists(full_dest) and os.path.isdir(full_src):
            if not mkdir_p(full_dest):
                error_trig("something went wrong")
    else:
        error_trig("backup.py: cannot stat '" + SRC + "': No such file or \
                directory")

def mkdir_p(dir_to_check):
    """
    provides functionality of mkdir -p
    """
    full_path = os.path.abspath(dir_to_check)
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return 1

    while True:
        feedback = input(dir_to_check + " doesn't exist, create it? [Y/n] ")
        if feedback == 'Y' or feedback == 'y':
            try:
                os.makedirs(full_path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(full_path):
                    pass
                else:
                    print("Error occurred:", exc.errno)
                    return 0

            return 1
        elif feedback == 'N' or feedback == 'n':
            error_trig("Please make destination or change it and try again.")
        else:
            print("Please enter Y(y) or n(N)")

def do_backup_wo_args():
    """
    does the backup if no arguments are provided
    """
    #TODO
    print("hi")

def do_backup_w_args():
    """
    does the backup if arguments are provided
    """
    backup()

def backup():
    """
    does the backup
    """
    print("backup")

def get_args(arg_list):
    """
    gets arguments from runtime
    """
    check_src = SRC
    check_dest = DEST
    err_check = ERR_FILE
    if arg_list:
        if "-h" or "--help" in arg_list:
            usage()
            exit(1)
        if "-s" in arg_list:
            spos = arg_list.index("-s")
            if len(arg_list) > spos:
                check_src = arg_list[spos + 1]
            else:
                error_trig("no path specified after '-s' option. Run with \
                        '-h' or '--help' for help")
        if "--src" in arg_list:
            spos = arg_list.index("--src")
            if len(arg_list) > spos:
                check_src = arg_list[spos + 1]
            else:
                error_trig("no path specified after '--src' option. Run with \
                        '-h' or '--help' for help")
        if "-d" in arg_list:
            dpos = arg_list.index("-d")
            if len(arg_list) > dpos:
                check_dest = arg_list[dpos + 1]
            else:
                error_trig("no path specified after '-d' option. Run with \
                        '-h' or '--help' for help")
        if "--dest" in arg_list:
            dpos = arg_list.index("--dest")
            if len(arg_list) > dpos:
                check_dest = arg_list[dpos + 1]
            else:
                error_trig("no path specified after '--dest' option. Run with \
                        '-h' or '--help' for help")
        if "-v" in arg_list:
            global SYNC_OPTS
            SYNC_OPTS = SYNC_OPTS.replace("q", "v")
        if "--verbose" in arg_list:
            global SYNC_OPTS
            SYNC_OPTS = SYNC_OPTS.replace("q", "v")
        if "-e" in arg_list:
            epos = arg_list.index("-e")
            if len(arg_list) > epos:
                err_check = arg_list[epos + 1]
            else:
                error_trig("no filename specified after '-e' option. Run \
                        with '-h' or '--help' for help")
        if "--err_file" in arg_list:
            epos = arg_list.index("--err_file")
            if len(arg_list) > epos:
                err_check = arg_list[epos + 1]
            else:
                error_trig("no filename specfied after '--err_file' option. \
                        Run with '-h' or '--help' for help")

    check_dirs()

    global ERR_FILE
    ERR_FILE = err_check

def main():
    """
    main function
    """
    get_args(argv[1:])

    if SRC == "" or DEST == "":
        do_backup_wo_args()
    else:
        do_backup_w_args()

    backup()

main()
