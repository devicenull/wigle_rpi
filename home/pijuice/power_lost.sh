#!/bin/bash

date >> /home/pijuice/power_lost.log
sudo /home/pijuice/power_lost_root.py >> /home/pijuice/power_lost.log 2>&1
