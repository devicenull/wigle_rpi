#!/bin/bash

# for old usb gps
#/usr/local/sbin/gpsd -b /dev/ttyUSB0
# for new serial gps
/usr/local/sbin/gpsd -b /dev/ttyS0 -s 115200
sleep 5
# Kismet tries to set these, but seems to fail
ip link set scanning0 down
iw scanning0 set monitor control
ip link set scanning0 up
sleep 5
/bin/systemctl start kismet
/bin/systemctl start ntp
