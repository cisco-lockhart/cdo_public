#! /usr/bin/env python

import requests
import base64
import json
import csv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import polling
import argparse
from termcolor import colored

DEVICES_ENDPOINT = 'services/targets/devices/'

token = input(colored("Enter your access token for CDO: ", 'cyan'))

use_default_url = input(colored("Use default https://defenseorchestrator.com url? [y] ", 'cyan'))
if use_default_url == "yes" or use_default_url == "y" or use_default_url == "":
  print("Using default url.")
  cdo_url = "https://defenseorchestrator.com"
else:
  cdo_url = input("Enter the url to use for CDO: ")

use_default_sdc = input(colored("Use the first listed SDC to connect to device? [y] ", 'cyan'))
if use_default_sdc == "yes" or use_default_sdc == "y" or use_default_sdc == "":
  print("Using the first SDC in list to connect to device.")
  sdc_index = 0
else:
  sdc_index = int(input(colored("Enter the index of the SDC to connect to the device: ", 'cyan')))


def cdo_query(url, method, body=None):
    query_url = cdo_url + '/aegis/rest/v1/' + url
    auth = "Bearer " + token
    headers = {'Accept': 'application/json',
               'Content-type': 'application/json',
               'Authorization': auth}
    try:
      req = requests.request(method, query_url, json=body, headers=headers)
      return req.json()
    except:
      print(colored("Error: Could not make request to given url: " + query_url, 'red'))


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
    print(colored('Creating device: %s' % name, 'yellow'))

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
        return print(colored('Failed to create device: %s' % name, 'red'))
    except polling.TimeoutException:
        return print(colored('Device never readied to receive credentials: %s' % name, 'red'))

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

    print(colored('Sending credentials to: %s' % name, 'yellow'))
    return cdo_query(DEVICES_ENDPOINT + ios_device['uid'], 'PUT', update_data)

def main():
    print(colored("Reading devices data...", "yellow"))
    with open('assets/devices.csv', 'r', encoding='utf-8') as f:
      reader = csv.reader(f)
      devices_list = list(reader)

    print(colored("Successfully read devices data!", "red"))

    proxy_response = cdo_query('services/targets/proxies', 'GET')
    if not proxy_response:
      print(colored("Did not receive response with SDCs", 'red'))
      quit()
    elif not proxy_response[sdc_index]:
      print(colored("Did not find an SDC at given index: " + sdc_index, 'red'))
      quit()
      
    try: 
      public_key = proxy_response[sdc_index]['larPublicKey']
      public_key_pem = base64.standard_b64decode(public_key['encodedKey'])
      key_id = public_key['keyId']
    except:
      raise Exception("Could not find encoded key from proxy response");

    [create_integration_device(device, public_key_pem, key_id) for device in devices_list]
    print(colored("Done!", 'green'))


main()