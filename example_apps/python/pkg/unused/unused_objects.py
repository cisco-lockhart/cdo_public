#!/usr/bin/env python

import requests
import json
import os
import sys
from ..utils import *

from .. import envutils
from sty import fg, ef, rs

NUM_OBJS_TO_RETRIEVE_PER_QUERY = 50

def view_unused_objects(api_token, env, output_file_name):
    num_unused_objs = _get_unused_obj_count(api_token, env)
    unused_objs_file = open(output_file_name, "w")
    unused_objects = []
    
    download_msg = as_in_progress_msg('Downloading information on ' + str(num_unused_objs) + ' unused objects from CDO environment: ' + env + '...')
    print(download_msg, end='\r')

    for i in range(0, num_unused_objs, NUM_OBJS_TO_RETRIEVE_PER_QUERY):
        params = {
            'q': '(issues:UNUSED) AND (cdoInternal:false) AND (isReadOnly:false)',
            'resolve': '[targets/objects.{uid, name}]',
            'limit': NUM_OBJS_TO_RETRIEVE_PER_QUERY,
            'offset': i
        }
        response = requests.get(url=envutils.get_objects_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)
        for obj in json.loads(response.text):
            unused_objects.append(obj['uid'])
            unused_objs_file.write(obj['uid'] + ', ' + obj['name'])
            unused_objs_file.write('\n')
    unused_objs_file.close()
    print(as_done_msg(download_msg))
    return unused_objects

def delete_unused_objects(api_token, env, output_file_name):
    i = 0
    unused_objects = view_unused_objects(api_token, env, output_file_name)
    for unused_obj_uid in unused_objects:
        delete_msg = as_in_progress_msg('Deleting unused object ' + str(i + 1) + '/' + str(len(unused_objects)) + ' from CDO environment: ' + env + '...')
        print(delete_msg, end='\r')
        response = requests.delete(url=envutils.get_object_url(env, unused_obj_uid),
                            headers=envutils.get_headers(api_token),
                            params={})
        i += 1
    print(as_done_msg(delete_msg))

def _get_unused_obj_count(api_token, env):
    # https://staging.dev.lockhart.io/aegis/rest/v1/services/targets/objects?agg=count&q=()
    params = {
        'q': '(issues:UNUSED) AND (cdoInternal:false) AND (isReadOnly:false)',
        'agg': 'count'
    }
    response = requests.get(url=envutils.get_objects_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)

    return json.loads(response.text)['aggregationQueryResult']