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

def TryComand(comand, TF):
    try:
        subprocess.call(comand, shell = TF)
        print(comand)
    except subprocess.CalledProcessError as e:
        print(comand)
        print(e.output)
        sys.exit(1)

if __name__ == "__main__":
    options = parse_args()
    setup_logging(options)

    try:
        
        logger.debug('start deleting')
        logger.debug('delete alias in bashrc for root')
        subprocess.call('sudo sed -i "/vulnf/d"  /root/.bashrc', shell = True)
        logger.debug('delete alias in bashrc for user')
        homefolder = os.path.join('/home/', os.environ['USER'])
        bashrc = os.path.abspath('%s/.bashrc' % homefolder)
        print('BBBBBAAAASHH=',bashrc)
        TryComand('sudo sed -i "/bmctester/d" ' + bashrc, True)
        logger.debug('delete all scripts files from /opt')
        TryComand('sudo rm -r /opt/bmc_tester', True)

    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)