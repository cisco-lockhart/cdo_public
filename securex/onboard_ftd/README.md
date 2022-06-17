# Onbaord FTD to CDO via SecureX

## Change Log

| Date | Notes |
|:-----|:------|
| June 15, 2022 | - Initial release |
| June 16, 2022 | - Updated documentation and reordered some if/then blocks |
  
---
## Usage
This workflow will onboard a Cisco Secure Firewall Threat Defense appliance (Physical or Virtual) into 
Cisco Defense Orchestrator and onboard the device into the CDO cloud delivered Firewall Management Center.

One may either trigger the workflow with a simple HTTP POST with a json payload or trigger the workflow manunually in SecureX Orchestration UI and manually submit the needed parameters.

Here is an example cURL to trigger the workflow. Note that the webhook URL will be specific to your SecureX instance as defined in your "webhooks" menu in SecureX. See [webhooks](#webhooks) below.
```
curl --location --request POST 'https://securex-ao.us.security.cisco.com/webhooks/your-webhook-url?api_key=your-webhook-api-key' \
--header 'Content-Type: application/json' \
--data-raw '{
    "device_name": "Your-Device-Name",
    "is_threat": true,
    "is_url": true,
    "is_malware": true,
    "ra_vpn": "",
    "is_virtual": true,
    "performance_tier": "FTDv10",
    "access_policy": "Default Access Control Policy",
    "cdo_api_key": "your cdo-api-key goes here"
}'
```

## Requirements
* The [targets](#targets) listed at the bottom of the page
* The [events](#events) listed at the bottom of the page
* The [webhooks](#webhooks) listed at the bottom of the page  
---

## Workflow Steps
1. If triggered by webhook populate varaibles using the parameters passed in the json payload POST. See [configuration](#configuration) for details on the variables
2. If not triggered by a webhook, the interactive user will need to input the values for the variables at runtime via the webform in SecureX Workflows.
3. Pre-Flight Checks and tasks (Any failure will halt the workflow with a workflow "Completed" with the Completion Type set to "Failed" and a description of the error.)
    * Check to make sure a device with the given name does not already exist in CDO/FMC.
    * Get the UID of the cloud delivered Firewall Management Center (cdFMC)
    * Get the domain id of the domain in the cdFMC.
    * Get a list of the access-policies in the domain of the cdFMC
    * Make sure the supplied access-policy name exists in the cdFMC
    * If a virtual performance tier was passed, set the varaible
    * If a threat, url, malware, or vpn license was requested, set the variables
    * If the device is virtual but no perfoirmance tier was passed, default the performance tier to FTDv (variable)
4. Add the device to CDO with the parameters discovered above.
5. Once the "add device" has been triggered in CDO, use the returned device UID to check the state of the device add operation until CDO has completed the add operation.
6. Trigger the "Add device to FMC"
7. Check the state of the "Add device to FMC" until it has completed
8. Extract the generated "add manager" string to paste into the FTD as generated_command
9. TODO: One could then continue this workflow or create an atomic to ssh to the FTD (if reachable) and paste the "generated_command" into the CLI.

---

## Configuration
* Set the `device_name` (required) input string variable to the name we wish to call the device in CDO/FMC. e.g. "Chicago-Primary" (Use dns friendly characters)
* Set the `is_threat` (optional) input boolean variable to indicate that we should provision a THREAT license. 
* Set the `is_url` (optional) input boolean variable to indicate that we should provision a THREAT license.
* Set the `is_malware` (optional) input boolean variable to indicate that we should provision a THREAT license.
* Set the `ra_vpn` (optional) input string variable to indicate which VPN license to provision ["VPNOnly", "PLUS", "APEX", "PLUS,APEX"]
* Set the `performance_tier` (optional) input string to indicate which performance tier license to provision.  ["FTDv5","FTDv10","FTDv20","FTDv30","FTDv50","FTDv100","FTDv"]
* Set the `access_policy` (required) input string variable of the name of the policy to apply to the FTD at initial provisioning. e.g. "Default Access Control Policy"
* Set the `cdo_api_key` (required) input string variable of the CDP API key to use to execute this workflow.

---

## Targets
Choose the target for the region for which you would like to create the devices with this workflow.

| Target Name | Type | Details | Account Keys | Notes |
|:------------|:-----|:--------|:-------------|:------|
| CDO-US | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `www.defenseorchestrator.com`<br />_Path:_ `/` | | |
| CDO-EMEA | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `defenseorchestrator.eu`<br />_Path:_ `/` | | |
| CDO-APJ | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `www.apj.cdo.cisco.com`<br />_Path:_ `/` | | |

## Events
| Event Name | Criteria | Webhook |
|:------------|:------------|:------------|
| EVENT-ONBOARD-FTD-CDO | | WEBHOOK-ONBOARD-FTD-CDO |

## Webhooks
| Event Name | Content-Type | Notes |  
|:------------|:------------|:------------|
| WEBHOOK-ONBOARD-FTD-CDO | appliaction/json | APIkey and URL avaiable in webhook UI |

---

## Account Keys
| Account Key Name | Type | Details | Notes |
|:-----------------|:-----|:--------|:------|
