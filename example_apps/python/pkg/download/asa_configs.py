#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs


NUM_DEVICES_TO_RETRIEVE_PER_QUERY = 50

def download_asa_configs(api_token, env, output_dir):

    download_msg = as_in_progress_msg('Downloading configurations for ASAs from CDO environment: ' + env + '...')
    print(download_msg, end='\r')

    params = {
        'q': '(deviceType:ASA)',
    }
    headers = {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url='https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/devices',
                            headers=headers,
                            params=params)

    print(as_done_msg(download_msg))

def _save_device_config(device_name, device_config, output_dir):
    output_file = open(os.path.join(output_dir, device_name), 'w')
    output_file.write(device_config)
