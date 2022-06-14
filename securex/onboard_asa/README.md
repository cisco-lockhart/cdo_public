# Onbaord ASA to CDO via SecureX

This workflow will take some basic import parameters and add the given ASA to your CDO tenant, based on the CDO API token provided.

Import this workflow into your SecureX tenant by going to "Orchestration" and clicking "import" and pointing to the provided json file.

One can also call this workflow by webhook. Here is a sample of the payload that would be required to call by webhook. Note that when you import the workflow, your webhook endpoint url and key will be different, so adjust as required.

```
curl --location --request POST 'https://securex-ao.us.security.cisco.com/webhooks/your-webhook-url?api_key=your-webhook-api-key' \
--header 'Content-Type: application/json' \
--data-raw '{
	"cdo_api_key": "[your cdo api key]",
	"device_name": "my-asa",
	"sdc_name": "CDO_cisco_my-SDC-1",
	"admin_username": "your-asa-username",
	"admin_password": "your-asa-password",
	"asa_ip": "10.10.10.10",
	"asa_port": 443,
	"ignore_certificate": false,
	"aws_api_key": "your-aws-lambda-api-key**"
}'
```


** If using an OnPrem SDC, there are cryptographic functions required that are not avaialble in the SecureX implementation of Python. As a result, for this POC workflow, we are calling an AWS API Gateway where a Python lambda is using the python library `pycrptodome` to encrypt the given credentials and then return the encrypted username and password. You will need to either replicate this functionality in AWS or your own onprem API or come up with another way to supply the encypted credentials to the SDC. For convience sake, I have included the python lambda script in this repo. AWS Lambda also does not natively support `pycryptodome`, so one would need to add a lanbda layer to bring this module to your lambda function.


