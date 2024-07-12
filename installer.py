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
def check_package_manager():
    """
    This function checks which package manager is available on the system.

    The function attempts to find the first available package manager from a list of common ones:
    'apt-get', 'yum', 'dnf', 'pacman', and 'zypper'. It does this by running the 'which' command
    for each package manager and checking the return code. If the return code is 0, it means the
    package manager is available and the function returns the name of the package manager. If no
    package manager is found, the function returns 'Unknown'.

    Parameters:
    None

    Returns:
    str: The name of the available package manager or 'Unknown' if no package manager is found.
    """
    package_managers = ['apt-get', 'yum', 'dnf', 'pacman', 'zypper']
    
    for pm in package_managers:
        result = subprocess.run(['which', pm], stdout=subprocess.PIPE)
        if result.returncode == 0:
            return pm
    return 'Unknown'

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

def installing():
    """
    This function is responsible for installing the necessary scripts and components for the Vulners finder.
    It first logs a debug message indicating the start of the base installation script. Then, it changes the
    permissions of the base installation script and executes it. After that, it determines the available
    package manager using the check_package_manager function. Depending on the package manager, it changes
    the permissions of the corresponding installation script and executes it. If no package manager is found,
    it logs an error message and exits the program.

    Parameters:
    None

    Returns:
    None
    """
    logger.debug('start basg script for base installing')
    subprocess.call('chmod +x ' + ip + '/bash_scripts/base_installig.sh', shell=True)
    subprocess.call('sh ' + ip + '/bash_scripts/base_installig.sh', shell=True)
    pm = check_package_manager()
    if pm == 'apt-get':
        subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/install_apt.sh', shell=True)
        subprocess.call('.' + ip + '/bash_scripts/install_apt.sh', shell=True)
    elif pm == 'yum':
        subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/install_yum.sh', shell=True)
        subprocess.call('.' + ip + '/bash_scripts/install_yum.sh', shell=True)
    elif pm == 'dnf':
        subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/install_dnf.sh', shell=True)
        subprocess.call('.' + ip + '/bash_scripts/install_dnf.sh', shell=True)
    elif pm == 'pacman':
        subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/install_pacman.sh', shell=True)
        subprocess.call('.' + ip + '/bash_scripts/install_pacman.sh', shell=True)
    elif pm == 'zypper':
        subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/install_zypper.sh', shell=True)
        subprocess.call('.' + ip + '/bash_scripts/install_zypper.sh', shell=True)
    elif pm == 'Unknown':
        logger.error("No package manager found. Please install one of the following: apt-get, yum, dnf, pacman, or zypper.")
        sys.exit(1)
    
if __name__ == '__main__':
    
    options = parse_args()
    setup_logging(options)
    
    try:
        print("start installation vulners finder")
        if options.install:
            print("start installing")
            installing()
            logger.debug("finish installation")
        elif options.update:
            print("start updating")
            logger.debug("check version")
            old, new = get_version()
            logger.debug('check version: %s, %s', old, new)  # for debug only
            if old =="not installed":
                print("Program not installed. Start installing")
                installing()
                logger.debug("finish installation")
            elif float(new) > float(old):
                logger.debug('update old scripts files from /opt')
                subprocess.call('sudo chmod +x ' + ip + '/bash_scripts/updater.sh', shell=True)
                subprocess.call('sh ' + ip + '/bash_scripts/updater.sh', shell=True)
                logger.debug("finish updating")
            logger.debug("last version installed")


    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)