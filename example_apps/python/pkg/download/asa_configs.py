#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs


NUM_DEVICES_TO_RETRIEVE_PER_QUERY = 50

def download_asa_configs(api_token, output_dir):

    download_msg = as_in_progress_msg('Downloading configurations for ASAs from CDO...')
    print(download_msg, end='\r')

    print(as_done_msg(download_msg))


def _save_device_config(device_name, device_config, output_dir):
    output_file = open(os.path.join(output_dir, device_name), 'w')
    output_file.write(device_config)
