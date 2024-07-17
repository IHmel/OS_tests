#!/usr/bin/python3
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])
pp = '/opt/vulnert' # installing programs path

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="BMC tester")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")

    base = parser.add_mutually_exclusive_group()    #main options
    base.add_argument("-r", "--run", help="start test", action="store_true")
    base.add_argument("-i", "--install", help="install scripts and components", action="store_true")
    base.add_argument("-rm", "--remove", help="remove script and components", action="store_true")
    base.add_argument("-c", "--config", help="configure script settings", action="store_true")
    
    g = parser.add_mutually_exclusive_group()   #debuginfo
    g.add_argument("-d", "--debug", action="store_true", default=False, help="enable debugging")
    g.add_argument("-s", "--silent", action="store_true", default=False, help="don't log to console")
    
    options = parser.add_argument_group("target options")
    options.add_argument('-t', '--target', help="target ip address")
    options.add_argument('-u', '--username', help="user to connect to bmc")
    options.add_argument('-p', '--password', help="password")

    return parser, parser.parse_args(args)

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

def check_ping(ip):
    response = os.popen(f"ping -c 5 {ip}").read()
    if "0% packet loss" in response:
        logging.debug(f"UP {ip} Ping Successful, Host is UP!")
        return True
    else:
        logging.debug(f"DOWN {ip} Ping Unsuccessful, Host is DOWN.")
        return False


if __name__ == "__main__":

    parser, options = parse_args()
    setup_logging(options)

    try:
        logger.debug("start bmc tester")
        if options.remove:
            subprocess.call('sh ' + pp + '/bash_scripts/deinstall.sh', shell=True)
        elif options.config:
            print("Configure function")
        elif options.run:
            print(f"""Run with next options:
                Target IP: {options.target};
                Username: {options.username}; 
                Password: {options.password}.""")
            if not check_ping(options.target):
                logging.debug("Check your network connection with target")
            else:
                subprocess.call('nmap -sV --script vuln ' + options.target, shell=True)
                print("start GRYAAZZZZ")
            
        else:
            parser.print_help()


    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)