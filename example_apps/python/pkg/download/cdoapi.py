#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs


NUM_DEVICES_TO_RETRIEVE_PER_QUERY = 50

PROD_URL = 'https://www.defenseorchestrator.com'


def get_devices(api_token):
    download_msg = as_in_progress_msg('Downloading configurations for ASAs from CDO...') 
    print(as_in_progress_msg(download_msg), end='\r')
    params = {
        'q': '(deviceType:ASA)',
    }
    headers = {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }

    response = requests.get(url=_build_url(namespace='targets', type='devices'),
                            headers=headers,
                            params=params)

    devices = json.loads(response.text)    
    print(as_done_msg(download_msg)) 
    return devices


def _build_url(namespace, type):
    return PROD_URL + '/aegis/rest/v1/services/' + namespace + '/' + type

def save_device_configs(devices, output_dir):
    for device in devices:
        _save_device_config(device['name'], device['deviceConfig'], output_dir)

def _save_device_config(device_name, device_config, output_dir):
    print(as_in_progress_msg('Saving ' + device_name +' to disk...'), end='')
    output_file = open(os.path.join(output_dir, device_name), 'w')
    output_file.write(device_config)
    print(as_done_msg(''))
