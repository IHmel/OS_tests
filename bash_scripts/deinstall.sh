#!/bin/bash
echo "Start deinstalling..."
echo "Delete user alis..."
sudo sed -i "/vulnf/d"  /home/"$(whoami)"/.bashrc
echo "Delete root alis..."
sudo sed -i "/vulnf/d"  /root/.bashrc
echo "Delete all sripts files"
sudo rm -r /opt/bmc_tester
echo "Delete /opt/vulnet"