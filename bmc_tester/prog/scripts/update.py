#!/usr/bin/python3
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

def get_version(path_bmc_tester):
    try:
        file = open("/opt/bmc_tester/version", "r")
        old = file.readlines(0)[0]
    except Exception:
        old = "not installed"
    path = path_bmc_tester+ '/prog/version'
    file = open(path, "r")
    new = file.readlines(0)[0]
    return old, new

def TryComand(comand, TF):
    try:
        subprocess.run(comand, shell = TF)
        print(comand)
    except subprocess.CalledProcessError as e:
        print(comand)
        print(e.output)
        sys.exit(1)

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="BMC tester")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")

    g = parser.add_mutually_exclusive_group()
    g.add_argument("-d", "--debug", action="store_true", default=False, help="enable debugging")
    g.add_argument("-s", "--silent", action="store_true", default=False, help="don't log to console")

    return parser.parse_args(args)

def setup_logging(options):
    """Configure logging."""
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(
            "%(levelname)s[%(name)s] %(message)s"))
        root.addHandler(ch)


if __name__ == "__main__":

    options = parse_args()
    setup_logging(options)
    try:
        logger.debug("check new version")
        print("""Specify the path to the BMC tester folder with the update. For example: /home/User/Download/bmc_tester """)
        path_to_update=str(input())
        old, new = get_version(path_to_update)

    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)