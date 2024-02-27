#!/bin/bash
sudo mount /run/user/1000/media/by-id-usb-JMicron_Tech_DD56419883914-0\:0-part1/Astra_linux/1.7/1.7.5* /media/cdrom/
sudo apt-get update
#Установка ядер
sudo apt install linux-5.4
sudo apt install linux-5.10
sudo apt install linux-5.15
sudo apt install linux-6.1
#Установка пакетов

apt-get install lshw
dpkg -i /home/user/pakets/libsctp1_1.0.18+dfsg-1_amd64.deb
dpkg -i /home/user/pakets/libiperf0_3.9-1_amd64.deb
dpkg -i /home/user/pakets/iperf3_3.9-1_amd64.deb
dpkg -i /home/user/pakets/libcpufreq0_008-2_amd64.deb
dpkg -i /home/user/pakets/cpufrequtils_008-2_amd64.deb
dpkg -i /home/user/pakets/libaio1_0.3.112-3_amd64.deb
dpkg -i /home/user/pakets/libipsec-mb0_0.52-2_amd64.deb
dpkg -i /home/user/pakets/stress-ng_0.09.50-1_amd64.deb
umount /media/cdrom/
echo -e "Освободите все USB разЪемы и нажмите любую кнопку"
read -n 1
mkdir /home/user/logs/
sh /home/user/scripts/astra_hard.sh

