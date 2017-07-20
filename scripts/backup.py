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
    print("Error:", message)
    exit(1)

def usage():
    print("Usage: backup.py [OPTIONS]")
    print("Examples:         backup.py -e err_file.txt -v")
    print("                  backup")
    print("Options:")
    print("-s, --src /src/dir            Source directory.")
    print("-d, --dest /dest/dir          Destination directory.")
    print("-h, --help                    Print this help.")
    print("-e, --err_file err_file.txt   Output errors to the provided file.")
    print("-v, --verbose                 Turns on verbose logging.")

def check_dir(dir):
    full_path = os.path.abspath(dir)
    if os.path.isdir(full_path) or os.path.isdir(full_path):
        return 1
    else:
        return 0

def do_backup_wo_args():
    #TODO
    print("hi")

def get_args(arg_list):
    check_dir = SRC
    err_check = ERR_FILE
    if arg_list:
        if "-h" or "--help" in arg_list:
            usage()
            exit(1)
        if "-s" in arg_list:
            spos = arg_list.index("-s")
            if len(arg_list) > spos:
                check_dir = arg_list[spos + 1]
            else:
                error_trig("no path specified after '-s' option. Run with \
                        '-h' or '--help' for help")
        if "--src" in arg_list:
            spos = arg_list.index("--src")
            if len(arg_list) > spos:
                check_dir = arg_list[spos + 1]
            else:
                error_trig("no path specified after '--src' option. Run with \
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
    else:
        do_backup_wo_args()

def main():
    get_args(argv[1:])

main()
