#!/bin/bash
mkdir /home/user/hard_logs
glxinfo | grep -i renderer > /home/user/hard_logs/info_renderer.txt
glxinfo -B > /home/user/hard_logs/glxinfo.txt
echo -e "ready for ipef?????"
read -n 1
script -c 'iperf3 -c 172.26.60.153 -P 50 -R -t 300' /home/user/hard_logs/ip_info.txt
script -c 'stress-ng -c 0 -m 0 -d 0 -i 0 -C 0 -B 0 -t 1h --tz --metrics-brief -v' /home/user/hard_logs/stressng.txt
7z b -mm=* > /home/user/hard_logs/7zip_1.txt
7z b -mm=* > /home/user/hard_logs/7zip_2.txt
7z b -mm=* > /home/user/hard_logs/7zip_3.txt
timeout 10.08m  glxgears -info > /home/user/hard_logs/glxgears_info.txt
sh /home/user/scripts/Astra_min.sh
 