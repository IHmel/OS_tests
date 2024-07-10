#!/usr/bin/python3
import configparser
import argparse
import sys
import logging
import logging.handlers
import os
import subprocess
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])



def TryComand(comand):
    subprocess.run(comand, shell = True)
    logger.debug(comand)
    

def installing():

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