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

with open('/home/pijuice/wigle.json', 'r') as f:
    wigleinfo = json.load(f)

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

requests_auth = requests.auth.HTTPBasicAuth(wigleinfo['username'], wigleinfo['password'])

logger.info('Internet connectivity found, looking for kismet logs')
for filename in glob.glob('/var/log/kismet/*.kismet'):
    logger.debug(filename)

    proc = subprocess.Popen(['kismetdb_to_wiglecsv', '--in', filename, '--out', '-', '--rate-limit', '3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode='wb') as out_f:
            shutil.copyfileobj(proc.stdout, out_f)
    for line in proc.stderr:
            logger.debug(line)
    proc.wait()
    if proc.returncode != 0:
        logger.info('wigle2csv returned %i, not uploading file' % proc.returncode)
        continue

    compressed.seek(0)
    with open('/tmp/last_upload.gz', 'wb') as f:
            shutil.copyfileobj(compressed, f)
    compressed.seek(0)
        
    try:
        result = requests.post('https://api.wigle.net/api/v2/file/upload', auth=requests_auth, files={'file': ('upload.csv.gz', compressed)}, data={"donate": True })
        result.raise_for_status()
        logger.info('Upload completed, deleting file')
        logger.info(result.text)
        os.remove(filename)
    except requests.exceptions.RequestException as e:
        logger.exception(e)

logger.info('Shutting down')
subprocess.call(['halt'])
