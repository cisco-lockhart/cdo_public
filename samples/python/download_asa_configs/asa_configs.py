#!/usr/bin/env python

import requests
import json
import os

US_BASE_URL="localhost:9000"
EU_BASE_URL="www.defenseorchestrator.eu"

GET_DEVICES_URL="http://{0}/aegis/rest/v1/services/targets/devices"

def download_asa_configs(api_token, env, output_dir):
    params = {
        'q': '(deviceType:ASA)',
        'resolve': '[targets/devices.{name,deviceConfig}]'
    }

    response = requests.get(url=_get_devices_url(env),
                            headers=_get_headers(api_token),
                            params=params)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    devices_json = json.loads(response.text)
    for device_json in devices_json:
        config_file = open(os.path.join(output_dir, device_json['name'] + '.config.txt'), "w")
        config_file.write(device_json['deviceConfig'])
        config_file.close()

def _get_headers(api_token):
    return {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
    }


def _get_devices_url(env):
    return GET_DEVICES_URL.format(_get_base_url(env))


def _get_base_url(env):
    if env == 'us':
        return US_BASE_URL
    else:
         return EU_BASE_URL
