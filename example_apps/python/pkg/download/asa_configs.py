#!/usr/bin/env python

from ..utils import *


def download_asa_configs(api_token, env, output_dir):
    download_msg = as_in_progress_msg('Downloading configurations for ' + str(num_devices) + ' ASAs from CDO environment: ' + env + '...')
    print(download_msg, end='\r')
    print(as_done_msg(download_msg))

