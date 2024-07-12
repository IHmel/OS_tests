#!/bin/bash
echo -e "Start updater.sh..."
echo -e "Copying all new programm files to /opt/vulnert"
echo -e "Copying bash_scripts"
sudo cp /bash_scripts/* /opt/vulnert/bash_scripts
echo -e "Copying dock"
sudo cp /dock/* /opt/vulnert/dock
echo -e "Copying python_scripts"
sudo cp /python_scripts/* /opt/vulnert/python_scripts
echo -e "Copying config_files"
sudo cp  /config_files/program.ini /opt/vulnert/config_files