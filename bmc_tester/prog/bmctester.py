#!/usr/bin/python3
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="BMC tester")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")

    base = parser.add_mutually_exclusive_group()
    base.add_argument("-r", "--run", help="start test", action="store_true")
    base.add_argument("-i", "--install", help="install scripts and components", action="store_true")
    base.add_argument("-u", "--update", help="update script and components", action="store_true")
    base.add_argument("-rm", "--remove", help="remove script and components", action="store_true")
    
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
            subprocess.call('rm -r /opt/bmc_tester', shell = True)
        elif options.install:
            logger.debug('create folder for script in /opt')
            subprocess.call('mkdir /opt/bmc_tester', shell = True)
            logger.debug('copy scripts files')
        elif options.update:
            print("update")

    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)