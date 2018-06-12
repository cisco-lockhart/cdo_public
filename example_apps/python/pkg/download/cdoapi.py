#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs

PROD_URL = 'https://www.defenseorchestrator.com'


def get_devices(api_token, offset=0, limit=50):
    download_msg = as_in_progress_msg('Downloading configurations for ASAs from CDO...') 
    print(as_in_progress_msg(download_msg), end='\r')
    params = {
        'q': '(deviceType:ASA)',
        'offset': offset,
        'limit': limit
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

def save_device_config(device, output_dir):
    print(as_in_progress_msg('Saving ' + device['device_name'] +' to disk...'), end='')
    output_file = open(os.path.join(output_dir, device['device_name']), 'w')
    output_file.write(device['deviceConfig'])
    print(as_done_msg(''))
