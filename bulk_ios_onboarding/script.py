#! /usr/bin/env python

import requests
import base64
import json
import csv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import polling
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help='the CDO url to use')
parser.add_argument('-t', '--token', type=str, help='the access token for CDO')
parser.add_argument('-s', '--sdcIndex', type=int, help='the index of the sdc to use based on response from lar proxy')
args = parser.parse_args()
CDO_ENDPOINT = args.url or "https://defenseorchestrator.com"
API_TOKEN = args.token.strip()
DEVICES_ENDPOINT = 'services/targets/devices/'
SDC_INDEX = args.sdcIndex or 0

def cdo_query(url, method, body=None):
    query_url = CDO_ENDPOINT + '/aegis/rest/v1/' + url
    auth = "Bearer " + API_TOKEN
    headers = {'Accept': 'application/json',
               'Content-type': 'application/json',
               'Authorization': auth}

    req = requests.request(method, query_url, json=body, headers=headers)
    return req.json()


def is_waiting_for_data(uid):
    device = cdo_query(DEVICES_ENDPOINT + uid, 'GET')
    return device['status'] == 'WAITING_FOR_DATA'


def encrypt_credential(public_key_pem, plain_text):
    public_key = RSA.importKey(public_key_pem)
    cipher = PKCS1_v1_5.new(public_key)
    encrypted_msg = cipher.encrypt(plain_text.encode('utf-8'))
    encoding = base64.standard_b64encode(encrypted_msg)
    return str(encoding, 'utf-8')


def create_integration_device(device, public_key_pem, key_id):
    name, host, port, username, password, enable_password = [device[i] for i in range(len(device))]
    print('Creating device: %s' % name)

    ipv4 = "%s:%s" % (host, port)
    post_body = {
        'model': 'false',
        'tags': {},
        'deviceType': 'IOS',
        'name': name,
        'ipv4': ipv4,
    }

    ios_device = cdo_query(DEVICES_ENDPOINT, 'POST', post_body)

    try:
        polling.poll(lambda: is_waiting_for_data(ios_device['uid']), step=.25, timeout=60)
    except KeyError:
        return print('Failed to create device: %s' % name)
    except polling.TimeoutException:
        return print('Device never readied to receive credentials: %s' % name)

    encrypted_username = encrypt_credential(public_key_pem, username)
    encrypted_password = encrypt_credential(public_key_pem, password)
    encrypted_enable_password = encrypt_credential(public_key_pem, enable_password) if isinstance(enable_password, str) else None
    encoded_creds = {
        'keyId': key_id,
        'username': encrypted_username,
        'password': encrypted_password,
        'enablePassword': encrypted_enable_password
    }

    update_data = {
        'credentials': json.dumps(encoded_creds),
        'stateMachineContext': {
            'acceptCert': 'true'
        }
    }

    print('Sending credentials to: %s' % name)
    return cdo_query(DEVICES_ENDPOINT + ios_device['uid'], 'PUT', update_data)


def main():
    proxy_response = cdo_query('services/targets/proxies', 'GET')
    public_key = proxy_response[SDC_INDEX]['larPublicKey']
    public_key_pem = base64.standard_b64decode(public_key['encodedKey'])
    key_id = public_key['keyId']

    with open('devices.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        devices_list = list(reader)

    [create_integration_device(device, public_key_pem, key_id) for device in devices_list]
    print("done")


main()