# Onbaord ASA to CDO via SecureX

This workflow will take some basic import parameters and add the given FTD to your CDO tenant and cloud delivered Firewall Management Center.

Import this workflow into your SecureX tenant by going to "Orchestration" and clicking "import" and pointing to the provided json file.

One can also call this workflow by webhook. Here is a sample of the payload that would be required to call by webhook. Note that when you import the workflow, your webhook endpoint url and key will be different, so adjust as required.

```
curl --location --request POST 'https://securex-ao.us.security.cisco.com/webhooks/your-webhook-url?api_key=your-webhook-api-key' \
--header 'Content-Type: application/json' \
--data-raw '{
    "device_name": "SATX-720-82-PRI",
    "is_threat": true,
    "is_url": true,
    "is_malware": true,
    "ra_vpn": "",
    "is_virtual": true,
    "performance_tier": "FTDv10",
    "access_policy": "Default Access Control Policy",
    "cdo_api_key": "your-cdo-api-key"
}'
```
