#!/usr/bin/python3
import configparser
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])
pp = '/opt/vulnert' # installing programs path
ip = os.getcwd() # installer path

def setup_logging(options):
    """
    Configure logging for the BMC tester script.

    This function sets up the logging configuration based on the provided options.
    It configures the root logger to output messages at the WARNING level and the logger
    for this script to output messages at the DEBUG or INFO level, depending on the
    value of the 'debug' option. If the 'silent' option is not set, it also adds a
    StreamHandler to the root logger to output messages to the console.

    Parameters:
    options (argparse.Namespace): An object containing the parsed command-line arguments.
        - options.debug (bool): If True, enable debugging mode.
        - options.silent (bool): If True, do not log to the console.

    Returns:
    None
    """
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(
            "%(levelname)s[%(name)s] %(message)s"))
        root.addHandler(ch)

def get_version():
    """
    This function retrieves the version numbers of the old and new versions of a program.

    Parameters:
    None

    Returns:
    tuple: A tuple containing two elements. The first element is the version number of the old program,
        and the second element is the version number of the new program. If the old program is not installed,
        the first element will be 'not installed'.
    """
    config_old = configparser.ConfigParser()
    config_new = configparser.ConfigParser()
    pd = '/config_files/program.ini'  # file with program version info

    try:
        config_old.read(pp + pd)    
        print(pp+pd)
        old = float(config_old['PROG']['version'])
    except Exception:
        old = 'not installed'

    config_new.read(ip + pd)
    new = float(config_new['PROG']['version'])

    return old, new

def parse_args(args=sys.argv[1:]):
    """
    Parses command-line arguments for the Vulners finder script.

    This function uses the argparse module to define and parse command-line arguments.
    It defines options for installing and updating scripts and components, as well as
    options for displaying the version numbers of the old and new programs. Additionally,
    it allows enabling debugging mode and suppressing console logging.

    Parameters:
    args (list, optional): A list of command-line arguments to be parsed.
        Defaults to sys.argv[1:] if not provided.

    Returns:
    argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(prog="Vulners finder")

    parser.add_argument("-i", "--install", help="install scripts and components", action="store_true")
    parser.add_argument("-up", "--update", help="remove script and components", action="store_true")

    old, new = get_version()    
    parser.add_argument("-nv", "--new_version", action="version", version="%(prog)s "+ str(new))
    parser.add_argument("-v", "--version", action="version", version="%(prog)s "+str(old))

    g = parser.add_mutually_exclusive_group()
    g.add_argument("-d", "--debug", action="store_true", default=False, help="enable debugging")
    g.add_argument("-s", "--silent", action="store_true", default=False, help="don't log to console")

    return parser.parse_args(args)

if __name__ == '__main__':
    
    options = parse_args()
    setup_logging(options)
    
    try:
        logger.debug("start bmc tester")
        if options.install:
            logger.debug("start installing")
            #start installing function
        elif options.update:
            logger.debug("check version")
            old, new = get_version(os.getcwd())
            if old =="not installed":
                logger.debug("start installing")
            #start installing function
            elif float(new) > float(old):
                logger.debug("start updating")
                logger.debug('delete old scripts files from /opt')
                TryComand('sudo rm -r /opt/bmc_tester/scripts')
                TryComand('sudo cp ' + os.getcwd() + '/prog/* /opt/bmc_tester/scripts')
                TryComand('sudo chmod +x /opt/bmc_tester')
                logger.debug("finish updating")
            logger.debug("last version installed")


    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)