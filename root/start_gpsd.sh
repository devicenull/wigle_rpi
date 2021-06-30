#!/bin/bash

# using a dev board here, see
# https://portal.u-blox.com/s/question/0D52p00009UDZxeCAH/changing-xplrm9-ftdi-interface-descriptor
/sbin/modprobe ftdi_sio
echo 1546 0501 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sleep 1
/bin/stty -F /dev/ttyUSB0 clocal raw speed 460800

/usr/local/sbin/gpsd -b /dev/ttyUSB0 --speed 460800
sleep 5
/bin/systemctl start kismet
/bin/systemctl start ntp

# work around issue where systemd starts writing to the journal
# before /var/log is mounted...
/bin/systemctl restart systemd-journald.service
/bin/systemctl restart rsyslogd.service
