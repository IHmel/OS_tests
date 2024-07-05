#!/usr/bin/python3
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

def get_version():
    try:
        file = open("/opt/bmc_tester/version", "r")
        old = file.readlines(0)[0]
    except Exception:
        old = "not installed"

    path = os.getcwd() + '/prog/version'
    file = open(path, "r")
    new = file.readlines(0)[0]

    return old, new

    

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="BMC tester")

    parser.add_argument("-i", "--install", help="install scripts and components", action="store_true")
    parser.add_argument("-rm", "--remove", help="remove script and components", action="store_true")

    old, new = get_version()    
    parser.add_argument("-nv", "--new_version", action="version", version="%(prog)s "+new)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s "+old)

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
        logger.debug("start bmc tester")
        if options.remove:
            logger.debug('delete scripts files from /opt')
            try:
                subprocess.call('rm -r /opt/bmc_tester', shell = False)
            except FileNotFoundError as e:
                logger.exception("%s", e)
                sys.exit(1)
            subprocess.call('unalias bmctester', shell = True)
            subprocess.call('sudo sed -i "/bmctester/d"  /root/.bashrc', shell = True)

            print("All files and aliases have been deleted")
        elif options.install:
            logger.debug('create folder for script in /opt')
            subprocess.call('mkdir /opt/bmc_tester', shell = True)
            logger.debug('copy scripts files')
            subprocess.call('cp ' + os.getcwd() + '/prog/* /opt/bmc_tester', shell = True)
            logger.debug('create alias')
            subprocess.call('chmod +x /opt/bmc_tester', shell = True)
            subprocess.call("alias bmctester='sudo ./opt/bmc_tester/bmctester.py'", shell = True)
            subprocess.call("echo \"alias bmctester='sudo ./opt/bmc_tester/bmctester.py'\" >>/root/.bashrc", shell = True)



        elif options.update:
            print("update")

    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)