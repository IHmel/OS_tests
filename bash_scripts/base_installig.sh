#!/bin/bash
echo -e "Start base installing..."
echo -e "Creating catalog /opt/vulnet"
sudo mkdir /opt/vulnert
echo -e "Copying all programm files to /opt/vulnert"
sudo cp -r /* /opt/vulnert
echo -e "changes the permissions of the files"
sudo chmod +x -r /opt/vulnert/*

echo -e "creating an alias for root"
if grep "alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'" /root/.bashrc; then
echo "alias has already been created"
else
sudo echo "alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'" >>/root/.bashrc
echo "alias created"
fi

echo -e "creating an alias for user"
if grep "alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'" /home/"$(whoami)"/.bashrc; then
echo "alias has already been created"
else
sudo echo "alias bmctester='sudo python /opt/bmc_tester/scripts/bmctester.py'" >>/home/"$(whoami)"/.bashrc
echo "alias created"
fi

echo -e "Finish base installing..."
