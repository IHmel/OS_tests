#!/usr/bin/python3
import configparser
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

def get_version(path_bmc_tester):
    """
    This function retrieves the current and new versions of the BMC tester.

    Parameters:
    path_bmc_tester (str): The path to the directory where the BMC tester is installed.

    Returns:
    tuple: A tuple containing the old version (str) and the new version (str).
    If the old version cannot be determined, "not installed" is returned.
    """
    config = configparser.ConfigParser()
    try:
        config.read('example.ini')
        file = open("/opt/bmc_tester/prog/data.ini", "r")
        old = config(["Program"]["version"])
    except Exception:
        old = "not installed"
    path = path_bmc_tester+ '/prog/version'
    file = open(path, "r")
    new = file.readlines(0)[0]
    return old, new

def TryComand(comand):
    subprocess.run(comand, shell = True)
    logger.debug(comand)
    

def installing():
    logger.debug('create folder for script in /opt')
    subprocess.call('sudo rm -r /opt/bmc_tester', shell = True)
    TryComand('sudo mkdir /opt/bmc_tester')

    logger.debug('copy scripts files')
    TryComand('sudo cp -r ' + os.getcwd() + '/* /opt/bmc_tester')
    TryComand('sudo chmod +x /opt/bmc_tester/scripts/*')
    
    logger.debug('create alias in bashrc for root')
    subprocess.call('sudo sed -i "/bmctester/d"  /root/.bashrc', shell = True)
    subprocess.call("sudo echo \"alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'\" >>/root/.bashrc", shell = True)

    logger.debug('create alias for user')
    homefolder = os.path.join('/home/', os.environ['USER'])
    bashrc = os.path.abspath('%s/.bashrc' % homefolder)
    print('BBBBBAAAASHH=',bashrc)
    alias = "alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'"
    with open(bashrc, 'r') as f:
        lines = f.readlines()
        if alias not in lines:
            out = open(bashrc, 'a')
            out.write(alias)

    logger.debug('check installing nmap')
    packet_manager = """Select a package manager. Enter:
                        1 for apt
                        2 for rpm
                        3 for yum"""
    print(packet_manager)
    pm = int(input())
    try:
        if pm == 1:
            apt()
        elif pm == 2:
            rpm()
        elif pm == 3:
            yum()
        else:
            print('Everything is broken')
    except Exception:
        print('Failed to install nmap. install it yourself: https://nmap.org/')


def parse_args(args=sys.argv[1:]):
    """
    Parse command-line arguments for the BMC tester script.

    Parameters:
    args (list, optional): A list of command-line arguments. Defaults to sys.argv[1:].

    Returns:
    argparse.Namespace: An object containing the parsed arguments.

    The function uses argparse to define and parse the command-line arguments.
    It supports the following options:
    -i, --install: Install scripts and components.
    -up, --update: Remove script and components.
    -nv, --new_version: Display the new version of the BMC tester.
    -v, --version: Display the current version of the BMC tester.
    -d, --debug: Enable debugging mode.
    -s, --silent: Do not log to the console.
    """
    parser = argparse.ArgumentParser(prog="BMC tester")

    parser.add_argument("-i", "--install", help="install scripts and components", action="store_true")
    parser.add_argument("-up", "--update", help="remove script and components", action="store_true")

    old, new = get_version()    
    parser.add_argument("-nv", "--new_version", action="version", version="%(prog)s "+new)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s "+old)

    g = parser.add_mutually_exclusive_group()
    g.add_argument("-d", "--debug", action="store_true", default=False, help="enable debugging")
    g.add_argument("-s", "--silent", action="store_true", default=False, help="don't log to console")

    return parser.parse_args(args)

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
    
def apt():
    subprocess.run("sudo apt-get update", shell = True)
    subprocess.run("sudo apt-get install nmap", shell = True)

def dnf():
    subprocess.run("sudo dnf update", shell = True)
    subprocess.run("sudo dnf install nmap -y", shell = True)

def yum():
    subprocess.run("sudo yum update", shell = True)
    subprocess.run("sudo yum install nmap", shell = True)


if __name__ == "__main__":

    options = parse_args()
    setup_logging(options)

    try:
        logger.debug("start bmc tester")
        if options.install:
            logger.debug("start installing")
            installing()
        elif options.update:
            logger.debug("check version")
            old, new = get_version(os.getcwd())
            if old =="not installed":
                installing()
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