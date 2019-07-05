import json

import requests

from ..utils import as_in_progress_msg, as_done_msg
from .. import envutils
from .delete_shadows import *


def perform_shadowed_action(api_token, env, query, delete=True):
    print(as_in_progress_msg('Finding ASA devices...'), end='')
    print('', end='\r')
    print(as_in_progress_msg('Finding ASA devices...'), end='')
    device_dict = _get_asas_by_query(api_token, env, query)
    print(as_done_msg(str(len(device_dict)) + ' found'))

    if delete:
        delete_all_shadows(env, api_token, device_dict)


def _get_asas_by_query(api_token, env, query):
    if query is None:
        params = {
            'q': '(deviceType:ASA)',
            'resolve': '[targets/devices.{uid}]'
        }
    else:
        params = {
            'q': '(deviceType:ASA) AND (' + query + ')',
            'resolve': '[targets/devices.{uid, name}]'
        }
    response = requests.get(url=envutils.get_devices_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)
    device_dict = dict((device_details['uid'], device_details['name']) for device_details in json.loads(response.text))

    return device_dict
