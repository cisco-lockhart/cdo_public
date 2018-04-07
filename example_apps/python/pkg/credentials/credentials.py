import getpass
import json

import requests
import sys

from .. import envutils
from ..utils import as_in_progress_msg, as_done_msg, as_error_msg


def update_credentials(api_token, env, username, query):
    password = getpass.getpass(prompt='Enter new password: ')
    print(as_in_progress_msg('Finding ASA devices by query...'), end='')
    print ('', end='\r')
    print(as_in_progress_msg('Finding ASA devices by query...'), end='')
    asa_uids = _get_asas_by_query(api_token, env, query)
    print(as_done_msg(str(len(asa_uids)) + ' found'))

    if len(asa_uids) > 0:
        print(as_in_progress_msg('Retrieving SDC public key...'), end='')
        try:
            _get_sdc_public_key(api_token, env)
            print(as_done_msg(''))
        except EnvironmentError:
            print(as_error_msg('failed'))
            sys.exit(-1)

def _get_asas_by_query(api_token, env, query):
    params = {
        'q': '(deviceType:ASA) AND (' + query + ')',
        'resolve': '[targets/devices.{uid}]'
    }
    response = requests.get(url=envutils.get_devices_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)
    asa_uids = []
    for device_details in json.loads(response.text):
        asa_details = _get_specific_device(api_token, env, device_details['uid'])
        asa_uids.append(asa_details['uid'])

    return asa_uids

def _get_sdc_public_key(api_token, env):
    params = {
        'q': 'larStatus:ACTIVE',
        'resolve': '[targets/proxies.{larPublicKey}]'
    }

    response = requests.get(url=envutils.get_proxies_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)

    response_json = json.loads(response.text)

    if len(response_json) == 0:
        raise EnvironmentError('No active SDC found')

    return response_json[0]['larPublicKey']

def _get_specific_device(api_token, env, device_uid):
    envutils.get_specific_device_url(env, device_uid)
    response = requests.get(url=envutils.get_specific_device_url(env, device_uid),
                            headers=envutils.get_headers(api_token))

    return json.loads(response.text)

