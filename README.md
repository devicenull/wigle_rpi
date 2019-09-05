Wifi Wardriving Scripts for a Raspberry Pi

Fairly hacky setup wise, unlikely to work for anyone else without modification.  This assumes

* Modern version of GPSD (manually compile from 3.19-dev)
* Modern version of Kismet
* USB GPS on /dev/ttyUSB0
* WPA Supplicant configured to auto-connect on wifi0
* Wifi Adapter for scanning on wifi1
* PIJuice HAT + configure to execute `/home/pijuice/power_lost.sh` on USB power loss
* log2ram installed, setup with a 1G /var/log size, and rsync enabled
