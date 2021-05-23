#!/usr/bin/env python3

import glob
import gzip
import io
import json
import logging
import os
import shutil
import subprocess
import sys

import requests
from pijuice import PiJuice

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/var/log/wigleuploader.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(console)
logger = logging.getLogger('')

logger.info('Pi lost power')

logger.info('Configuring auto power on')
pj=PiJuice(1,0x14)
pj.power.SetWakeUpOnCharge(0.0)

subprocess.call(['service', 'kismet', 'stop'])

logger.info('Checking for internet connectivity')
internet_up = False
for i in range(0,10):
    try:
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.PIPE)
        internet_up = True
        break
    except subprocess.CalledProcessError:
        pass

if not internet_up:
    logger.info('No internet found, not uploading logs')
    subprocess.call(['halt'])
    sys.exit(0)


logger.info('Copying logs to HTPC')
proc = subprocess.Popen(['/usr/bin/rsync', '-rt', '--progress', '/var/log/kismet/', 'rsync://wiglepi@htpc.meltbeforefailure.com/wiglepi', '--password-file=/etc/rsync.password'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = proc.communicate()
logger.debug(stdout)
logger.debug(stderr)
if proc.returncode == 0:
    for filename in glob.glob('/var/log/kismet/*.kismet*'):
        logger.debug('Deleting %s' % filename)
        os.remove(filename)
else:
    logger.info('Rsync returned non-zero, not deleting logs')

logger.info('Shutting down')
subprocess.call(['halt'])
