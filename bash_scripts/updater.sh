#!/bin/bash
echo "Start updater.sh..."
echo "Copying all new programm files to /opt/vulnert"
echo "Copying bash_scripts"
sudo cp bash_scripts/* /opt/vulnert/bash_scripts
echo "Copying dock"
sudo cp dock/* /opt/vulnert/dock
echo "Copying python_scripts"
sudo cp python_scripts/* /opt/vulnert/python_scripts
echo "Copying config_files"
sudo cp  config_files/program.ini /opt/vulnert/config_files