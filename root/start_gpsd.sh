#!/bin/bash
/usr/local/sbin/gpsd -b /dev/ttyUSB0
sleep 5
/bin/systemctl start kismet
/bin/systemctl start ntp
