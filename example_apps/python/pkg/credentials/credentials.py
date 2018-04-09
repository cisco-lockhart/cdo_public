import getpass
import json

import requests
import sys

import time

from .. import envutils
from ..utils import as_in_progress_msg, as_done_msg, as_error_msg
from ..credentials import *
from ..crypto import *


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
            public_key = _get_sdc_public_key(api_token, env)
            print(as_done_msg(''))
        except EnvironmentError:
            print(as_error_msg('failed'))
            sys.exit(-1)

        encrypted_username = crypto.encrypt(public_key['encodedKey'], username)
        encrypted_password = crypto.encrypt(public_key['encodedKey'], password)

        _trigger_bulk_update_credentials(api_token, env, asa_uids, encrypted_username, encrypted_password,
                                         public_key['keyId'])

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

def _trigger_bulk_update_credentials(api_token, env, asa_uids, encrypted_username, encrypted_password, keyId):
    print(as_in_progress_msg('Updating credentials on ' + str(len(asa_uids)) + ' devices...'), end='')
    print('', end='\r')
    print(as_in_progress_msg('Updating credentials on ' + str(len(asa_uids)) + ' devices...'), end='')
    obj_refs = []
    for asa_uid in asa_uids:
        obj_refs.append({
            'uid': asa_uid,
            'namespace': 'asa',
            'type': 'configs'
        })
    job_context = {
        'credentials': json.dumps({
            'username': encrypted_username,
            'password': encrypted_password,
            'keyId': keyId
        })
    }

    job_data = {
        'action': 'UPDATE_CREDENTIALS',
        'objRefs': obj_refs,
        'jobContext': job_context,
        'triggerState': 'PENDING_ORCHESTRATION'
    }

    response = requests.post(envutils.get_jobs_url(env),
                             headers=envutils.get_headers(api_token),
                             json=job_data)

    job_uid = json.loads(response.text)['uid']
    is_done = False
    is_error = False

    while not (is_done or is_error):
        time.sleep(3)
        params = {
            'resolve': '[state-machines/jobs.{overallProgress}]'
        }
        query_response = requests.get(envutils.get_jobs_url(env) + '/' + job_uid,
                                      headers=envutils.get_headers(api_token),
                                      params=params)
        overall_progress = json.loads(query_response.text)['overallProgress']
        is_done = overall_progress == 'DONE'
        is_error = overall_progress == 'ERROR'

    if is_error:
        print(as_error_msg('failed to update credentials on some devices'))
    else:
        print(as_done_msg(''))

