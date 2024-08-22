#! /usr/bin/env python

import requests
import csv
from termcolor import colored
import inquirer
import typing
from tqdm import tqdm

REGIONS = {
    "US": "https://edge.us.cdo.cisco.com",
    "EU": "https://edge.eu.cdo.cisco.com",
    "APJ": "https://edge.apj.cdo.cisco.com",
    "Australia": "https://edge.aus.cdo.cisco.com",
    "India": "https://edge.in.cdo.cisco.com",
    # FOR TESTING:    "CI": "https://edge.ci.cdo.cisco.com",
}

def cdo_query(cdo_url, token, url, method, body=None):
    query_url = cdo_url + url
    auth = f"Bearer {token}" 
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": auth,
    }

    try:
        req = requests.request(method, query_url, data=body, headers=headers)
        if req.ok:
            return req.json()
        else:
            raise Exception(f"Got non 200 status code from request: {req.status_code}")
    except Exception as e:
        print(
      colored(f"Error: Could not make request to given url: {query_url}, due to: {e}", "red")
        )
        raise Exception("Failed to make request, check output for details")
    


def create_integration_device(cdo_url, token, device, proxy_name):
    name, host, port, username, password = [device[i] for i in range(len(device))]
    print(colored(f"Creating device: {name}", "yellow"))

    payload = f"""{{
        "name": "{name}",
        "deviceAddress": "{host}:{port}",
        "username": "{username}",
        "password": "{password}",
        "ignoreCertificate": false,
        "connectorName": "{proxy_name}",
        "labels": {{ }}
    }}"""

    cdo_query(cdo_url, token, "/api/rest/v1/inventory/devices/ios", "POST", payload)

def main():
    print(colored("Reading devices data...", "yellow"))
    with open("assets/devices.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        devices_list = list(reader)

    print(colored("Successfully read devices data!", "red"))

    token_field = "token"
    region_field = "region"
    questions = [
        inquirer.Password(token_field, message="Enter your access token for CDO"),
        inquirer.List(
            region_field,
            message="What region is your tenant in?",
            choices=[*REGIONS.keys()],
            default="US",
        ),
    ]
    token_and_region = typing.cast(
        typing.Dict, inquirer.prompt(questions, raise_keyboard_interrupt=True)
    )
    token = token_and_region[token_field]
    region = token_and_region[region_field]
    cdo_url = REGIONS[region]
    proxy_response = typing.cast(
        typing.List,
        cdo_query(cdo_url, token, "/aegis/rest/v1/services/targets/proxies", "GET"),
    )
    
    proxy_names = [p["name"] for p in proxy_response]

    sdc_name_field = "sdc_name"
    questions = [
        inquirer.List(
            sdc_name_field,
            message="Which SDC would you like to use?",
            choices=proxy_names,
        ),
    ]

    sdc_name_dict = typing.cast(
        typing.Dict, inquirer.prompt(questions, raise_keyboard_interrupt=True)
    )
    sdc_name = sdc_name_dict[sdc_name_field]

    for device in tqdm(devices_list):
      create_integration_device(cdo_url, token, device, sdc_name)
    print(colored("Done!", "green"))


main()
