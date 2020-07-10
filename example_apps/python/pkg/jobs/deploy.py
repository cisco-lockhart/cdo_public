from .. import envutils
from ..utils import *
import requests
import json

def deploy_to_devices(api_token, env, query):
    device_uids = get_device_uids(api_token, env, query)
    obj_refs = [{'uid': uid, 'namespace': 'targets', 'type': 'devices'} for uid in device_uids]

    in_progress_msg = as_in_progress_msg('Triggering deploy to ' + str(len(device_uids)) + ' devices in env ' + env)
    print(in_progress_msg, end='\r')
    data = json.dumps({
            'action': 'WRITE',
            'objRefs': obj_refs,
            'triggerState': 'PENDING_ORCHESTRATION'
        })
    response = requests.post(url=envutils.get_jobs_url(env),
        data = data,
        headers=envutils.get_headers(api_token))

    if response.status_code == 200:
        job_uid = json.loads(response.text)['uid']
        
        job_done = False
        while not job_done:
            job_status = get_job_status(api_token, env, job_uid)
            if job_status == 'DONE':
                job_done = True
                print(as_done_msg(in_progress_msg))
            elif job_status == 'ERROR':
                job_done = True
                print(as_error_msg(in_progress_msg))
    else:
        response.raise_for_status()
    

    print(as_done_msg(in_progress_msg))

def get_job_status(api_token, env, job_uid):
    response = requests.get(url=envutils.get_job_url(env, job_uid), headers=envutils.get_headers(api_token))
    return json.loads(response.text)['overallProgress']

def get_device_uids(api_token, env, query):
    in_progress_msg = as_in_progress_msg('Getting device UIDs to deploy to in env ' + env)
    print(in_progress_msg, end='\r')
    
    params = {
        'q': query,
        'resolve': '[targets/devices.{uid}]',
    }

    response = requests.get(url=envutils.get_devices_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)
    
    devices_json = json.loads(response.text)
    device_uids = [device_json['uid'] for device_json in devices_json]
    print(as_done_msg(in_progress_msg))
    return device_uids
