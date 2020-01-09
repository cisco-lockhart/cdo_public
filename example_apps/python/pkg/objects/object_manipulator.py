import json

from .. import envutils
from ..utils import *
import requests

def create_network_object_group(api_token, env, name, ips, device_type):
    in_progress_msg = as_in_progress_msg('Creating network object group with name ' + name)
    print(in_progress_msg, end='\r')
    if device_type is not 'ASA':
        print(as_error_msg(in_progress_msg))
        print(as_error_msg('Only device Type ASA supported right now.'))
    contents = list(map(lambda ip: {
        '@type': 'NetworkContent',
        'sourceElement': ip
    }, ips))
    data = json.dumps({
        'name': name,
        '@typeName': 'LocalObject',
        'objectType': 'NETWORK_GROUP',
        'contents': contents,
        'deviceType': device_type
    })
    response = requests.post(url=envutils.get_objects_url(env), data=data, headers=envutils.get_headers(api_token))

    if response.status_code == 200:
        object_uid = json.loads(response.text)['uid']
        print(as_done_msg(in_progress_msg + ' (UID: ' + object_uid + ')'))
    else:
        print(as_error_msg(in_progress_msg))
        response.raise_for_status()

def create_network_object(api_token, env, name, ip, device_type):
    data = json.dumps({
        'name': name,
        '@typeName': 'LocalObject',
        'objectType': 'NETWORK_OBJECT',
        'contents': [
            {
                '@type': 'NetworkContent',
                'sourceElement': ip
            }
        ],
        'deviceType': device_type
    })

    in_progress_msg = as_in_progress_msg('Creating network object with name ' + name)
    print(in_progress_msg, end='\r')
    response = requests.post(url=envutils.get_objects_url(env), data=data, headers=envutils.get_headers(api_token))

    if response.status_code == 200:
        object_uid = json.loads(response.text)['uid']
        print(as_done_msg(in_progress_msg + ' (UID: ' + object_uid + ')'))
    else:
        print(as_error_msg(in_progress_msg))
        response.raise_for_status()

