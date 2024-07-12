#!/bin/bash
echo "Start base installing..."
pwd
echo "Creating catalog /opt/vulnet"
sudo mkdir /opt/vulnert
sudo chmod 777 /opt/vulnert
echo "Copying all programm files to /opt/vulnert"
cp -r * /opt/vulnert
echo "changes the permissions of the files"
sudo chmod +x /opt/vulnert/python_scripts/*
sudo chmod +x /opt/vulnert/bash_scripts/*
sudo chmod +x /opt/vulnert/python_scripts/*

echo "creating an alias for root"
if sudo bash -c "grep vulnf /root/.bashrc"; then
echo "alias has already been created"
else
sudo bash -c "echo alias vulnf=\'python /opt/vulnert/python_scripts/main.py\' >> /root/.bashrc"
echo "alias created"
fi

echo "creating an alias for user"
if grep vulnf /home/"$(whoami)"/.bashrc; then
echo "alias has already been created"
else
echo alias vulnf=\'python /opt/vulnert/python_scripts/main.py\' >> /home/"$(whoami)"/.bashrc
echo "alias created"
fi

echo "Finish base installing..."
