# CDO-WF001 - Run ASA Macros by Device Tag

## Change Log

| Date | Notes |
|:-----|:------|
| June 23, 2022 | - Initial release |
| July 05, 2022 | - Added target group for all regions <br/> - Added input variable for dynamic region selection at rumtime|  
---
## Usage
This workflow will identify ASA devices that are tagged with the given tag as defined by the inpu parameter `cdo_tag` and will attempt to execute a macro identified by the input parameter `macro`. Once the macro has been executed on a device, the workflow will then attempt to log to a Mongo Atlas database the output from the macro (command) executed on the given ASA. 

One may either trigger the workflow with a simple HTTP POST with a json payload or trigger the workflow manunually in SecureX Orchestration UI and manually submit the needed parameters.
Import this workflow into your SecureX tenant by going to "Orchestration" and clicking "import" and pointing to the provided json file.

Here is an example cURL to trigger the workflow. Note that the webhook URL will be specific to your SecureX instance as defined in your "webhooks" menu in SecureX. See [webhooks](#webhooks) below.
```
curl --location --request POST 'https://securex-ao.us.security.cisco.com/webhooks/your-webhook-url?api_key=your-webhook-api-key' \
--header 'Content-Type: application/json' \
--data-raw '{
  "cdo_api_key": "[your cdo api key]",
  "cdo_region": "[CDO]-US",
  "cdo_tag": "your cdo tag",
  "macro": "your macro name in cdo",
  "mongo_atlas_data_source": "YourDatasource",
  "mongo_atlas_database": "yourdatabase",
  "mongo_atlas_collection": "yourcollection",
  "mongo_atlas_api": "/app/data-foo/endpoint/data/beta"
  "mongo_atlas_api_key": "xxxxx",
}'
```

## Requirements
* The [targets](#targets) listed at the bottom of the page
* The [events](#events) listed at the bottom of the page
* The [webhooks](#webhooks) listed at the bottom of the page
* A `cdo_api_key` with admin permissions in CDO passed as an input parameter to the workflow/webhook
* A `mongo_atlas_database`, `mongo_atlas_collection`, `mongo_atlas_api`, and `mongo_atlas_api_key` from a Mongo Atlas `mongo_atlas_data_source` (Free tier works just fine) passed as an input parameter to the workflow/webhook

---

## Workflow Steps
1. If triggered by webhook populate input varaibles using the parameters in the json payload POST. See [configuration](#configuration) for details on the variables
2. If not triggered by a webhook, the interactive user will need to input the values for the variables at runtime via the webform in SecureX Workflows.
3. Pre-Flight Checks and tasks (Any failure will halt the workflow with a workflow "Completed" with the Completion Type set to "Failed" and a description of the error.)


---

## Configuration
* Set the `cdo_api_key` (required) input string variable to the CDO API key we will use to execute this workflow
* Set the `cdo_region` (required) input string variable to the CDO region we wish to execute against \["[CDO]-US", "[CDO]-EMEA", "[CDO]-APJ"\]
* Set the `cdo_tag` (required) input string to the CDO tag applied to devices on which we wish to run the given `macro`
* Set the `macro` (required) input string variable to the name of the macro we wish to run on the devices that posess the tag `cdo_tag`
* Set the `mongo_atlas_data_source` (optional) input string variable to the DataSouce defined in Mongo Atlas
* Set the `mongo_atlas_database` (optional) input string input string variable to the DataBase we wish to write to as defined in Mongo Atlas
* Set the `mongo_atlas_collection` (optional) input string input string variable to the DataBase we wish to write to as defined in Mongo Atlas
* Set the `mongo_atlas_api` (optional) input string input string variable to the Mongo Atlas API endpoint path e.g. `/app/data-foo/endpoint/data/beta`
* Set the `mongo_atlas_collection` (optional) input string input string variable to the DataBase we wish to write to as defined in Mongo Atlas
* Set the `mongo_atlas_api_key` (optional) input string variable of the Mongo Atlas API key used to write to the Mongo Atlas Database

---
## SecureX Workflow Global Settings
### Targets
Target Groups are used to define the region for which you would like to execute this workflow at runtime.

| Target Group Name | Type | Selected Targets | Account Keys | Notes |
|:------------|:-----|:--------|:-------------|:------|
| CDO-ALL-Regions | HTTP Endpoint | `CDO-US`, `CDO-EMEA`, `CDO-APJ` | | |

| Target Name | Type | Details | Account Keys | Notes |
|:------------|:-----|:--------|:-------------|:------|
| CDO-US | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `www.defenseorchestrator.com`<br />_Path:_ `/` | No Account Keys | |
| CDO-EMEA | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `defenseorchestrator.eu`<br />_Path:_ `/` | No Account Keys | |
| CDO-APJ | HTTP Endpoint | _Protocol:_ `HTTPS`<br />_Host:_ `www.apj.cdo.cisco.com`<br />_Path:_ `/` | No Account Keys | |

---

### Events
| Event Name | Criteria | Webhook |
|:------------|:------------|:------------|
| EVENT-ONBOARD-FTD-CDO | | WEBHOOK-ONBOARD-FTD-CDO |
  
---  

### Webhooks
| Event Name | Content-Type | Notes |  
|:------------|:------------|:------------|
| WEBHOOK-XXX | appliaction/json | APIkey and URL avaiable in webhook UI |

---

### Account Keys
| Account Key Name | Type | Details | Notes |
|:-----------------|:-----|:--------|:------|

(None: CDO API key provided at runtime via input variables)