import json

import requests

from ..utils import as_in_progress_msg, as_done_msg, as_error_msg
from .. import envutils


def delete_all_shadows(env, api_token, device_dict):
    print(as_in_progress_msg('Finding access groups for selected ASAs...'), end='')
    print('', end='\r')
    print(as_in_progress_msg('Finding access groups for selected ASAs...'), end='')
    params = {
        'q': '(' + ' OR '.join(['deviceUid:' + device_uid for device_uid in list(device_dict.keys())]) + ')',
        'resolve': '[targets/accessgroups.{name,accessRules,deviceUid}]'
    }

    response = requests.get(url=envutils.get_access_groups_url(env),
                            headers=envutils.get_headers(api_token),
                            params=params)
    response_json = json.loads(response.text)

    print(as_done_msg(str(len(response_json)) + ' found'))

    for access_group in response_json:
        access_rules = access_group['accessRules']

        unshadowed_access_rules = []
        print(as_in_progress_msg('Detecting shadowed rules in access group ' + access_group['name'] + ' on device ' + device_dict.get(access_group['deviceUid']) + '...'), end='')
        for access_rule in access_rules:
            is_shadowed = False
            if access_rule['issues'] is not None and len(access_rule['issues']) > 0:
                for issue in access_rule['issues']:
                    if issue['issueType'] == 'SHADOWED':
                        is_shadowed = True
                        break
            if not is_shadowed:
                unshadowed_access_rules.append(access_rule)
        print(as_done_msg(''))

        num_shadows = len(access_rules) - len(unshadowed_access_rules)

        if num_shadows > 0:
            print(as_in_progress_msg(
                'Deleting ' + str(num_shadows) + ' shadowed access rules from access group ' + access_group['name'] + ' in device ' + device_dict.get(access_group['deviceUid'])), end='')
            print('', end='\r')
            print(as_in_progress_msg(
                'Deleting ' + str(num_shadows) + ' shadowed access rules from access group ' + access_group['name'] + ' in device ' + device_dict.get(access_group['deviceUid'])), end='')

            update_data = {
                'accessRules': unshadowed_access_rules
            }
            response = requests.put(url=envutils.get_access_groups_url(env) + '/' + access_group['uid'],
                                    headers=envutils.get_headers(api_token),
                                    json=update_data)

            if response.status_code == 200:
                print(as_done_msg(''))
            else:
                print(as_error_msg(''))
