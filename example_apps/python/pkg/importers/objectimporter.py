import requests
from .. import envutils
import json
import requests

def import_objects(api_token, env, csv_file_name):
    # params = {
    #     'q': '(objectType:*NETWORK*)',
    #     'limit': '171',
    #     'offset': '0'
    # }
    # objects_response = requests.get(url=envutils.get_objects_url(env),
    #                                 headers=envutils.get_headers(api_token),
    #                                 params=params)
    #
    # objects = json.loads(objects_response.text)
    #
    # csv_lines = []
    #
    # for obj in objects:
    #
    #     obj_name = obj['name']
    #     members = []
    #     for content in obj['contents']:
    #         if content['@type'] == 'NetworkContent':
    #             members.append(content['sourceElement'])
    #         else:
    #             members.append(content['name'])
    #
    #     csv_lines.append(obj_name + '\t' + ",".join(members) + '\t' + 'network\tFTD\n')
    #
    # to_write = open('/Users/siddhuwarrier/Documents/Customer_network.csv', 'w')
    # to_write.writelines(csv_lines)
    # to_write.close()

    csv = open(csv_file_name, 'r').read()
    post_params = {
        'csv': csv
    }

    object_csv = requests.post(envutils.get_object_csv_url(env),
                               json=post_params,
                               headers=envutils.get_headers(api_token))

    uid = json.loads(object_csv.text)['uid']
    put_params = {
        'triggerState': 'PENDING_UPLOAD_OBJECTS'
    }
    requests.put(envutils.get_object_csv_url(env) + '/' + uid,
                                   json=put_params,
                                   headers=envutils.get_headers(api_token))
