#!/bin/bash
REL="$(uname -r)"
mkdir /home/user/logs/$REL/
astra-create-debug-logs
mv /tmp/astra-logs* /home/user/logs/$REL/
lshw -html -sanitize -numeric > /home/user/logs/$REL/lshw_info.html
lspci -v | grep -i VGA > /home/user/logs/$REL/vga_adapter.txt
lspci -k | grep -EA2 'VGA|3D' > /home/user/logs/$REL/vga_driver.txt
aplay -l > /home/user/logs/$REL/audio_info.txt
cat /proc/cpuinfo > /home/user/logs/$REL/base_cpu.txt
lscpu > /home/user/logs/$REL/info_lscpu.txt
cpufreq-info > /home/user/logs/$REL/info_cpufreq.txt
xrandr > /home/user/logs/$REL/xrandr_info.txt
cp /home/user/hard_logs/*  /home/user/logs/$REL/