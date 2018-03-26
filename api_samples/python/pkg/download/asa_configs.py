#!/usr/bin/env python

import requests
import json
import os
from .. import envutils

GET_DEVICES_URL = "{0}/aegis/rest/v1/services/targets/devices"

NUM_DEVICES_TO_RETRIEVE_PER_QUERY = 50

def download_asa_configs(api_token, env, output_dir):
    num_devices = _get_device_count(env, api_token)

    print "Downloading configurations for " + str(num_devices) + " ASAs in env " + env

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
            config_file.write(device_json['deviceConfig'])
            config_file.close()
            print "Downloaded config for device " + device_json['name']


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
