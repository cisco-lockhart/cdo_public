#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs

GET_DEVICES_URL = "{0}/aegis/rest/v1/services/targets/devices"

NUM_DEVICES_TO_RETRIEVE_PER_QUERY = 50

def download_asa_configs(api_token, env, output_dir):
    num_devices = _get_device_count(env, api_token)

    download_msg = as_in_progress_msg('Downloading configurations for ' + str(num_devices) + ' ASAs from CDO environment: ' + env + '...')
    print(download_msg, end='\r')

    filenames = []
    animation = '|/-\\'
    for i in range(0, num_devices, NUM_DEVICES_TO_RETRIEVE_PER_QUERY):
        params = {
            'q': '(deviceType:ASA)',
            'resolve': '[targets/devices.{name,deviceConfig}]',
            'sort': 'name:desc',
            'limit': NUM_DEVICES_TO_RETRIEVE_PER_QUERY,
            'offset': i
        }

        response = requests.get(url=_get_devices_url(env),
                                headers=_get_headers(api_token),
                                params=params)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        devices_json = json.loads(response.text)
        for device_json in devices_json:
            config_file = open(os.path.join(output_dir, device_json['name'] + '.config.txt'), "w")
            if device_json['deviceConfig'] is not None:
                config_file.write(device_json['deviceConfig'])
            config_file.close()
            filenames.append(config_file.name)


            print(display_in_progress_animation(download_msg, i), end='\r')

    print(as_done_msg(download_msg))
    return filenames


def _get_device_count(env, api_token):
    params = {
        'q': '(deviceType:ASA)',
        'agg': 'count'
    }
    response = requests.get(url=_get_devices_url(env),
                            headers=_get_headers(api_token),
                            params=params)

    return json.loads(response.text)['aggregationQueryResult']


def _get_headers(api_token):
    return {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }


def _get_devices_url(env):
    return GET_DEVICES_URL.format(envutils.get_base_url(env))
