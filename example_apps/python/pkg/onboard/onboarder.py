#!/usr/bin/env python

import os
import requests

from .. import envutils
from ..utils import *


def upload_asa_configs(api_token, env, config_dir):
    config_files = os.listdir(config_dir)

    for i in range(0, len(config_files)):
        upload_config_msg = as_in_progress_msg('Creating model device ' + config_files[i])
        print(upload_config_msg, end='')
        config = open(os.path.join(config_dir, config_files[i]), 'r').read()
        json = {
            'name': config_files[i],
            'config': config,
            'deviceConfig': config,
            'model': True,
            'deviceType': 'asa'
        }
        response = requests.post(url=envutils.get_devices_url(env),
                                headers=envutils.get_headers(api_token),
                                json=json)
        if (response.status_code == 200):
            print(as_done_msg(''))
        else:
            print(as_error_msg(''))
            print(response.text)

