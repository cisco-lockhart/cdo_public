# set the token environment variable
```
TOKEN=xxxyyyzzz.xxxyyyzzz
```

# get the device UID
```
curl "https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/devices?q=name:Hollis*" -H "Authorization: Bearer $TOKEN" | jq -r '.[].uid'
```

# get the config summary, and the stagedConfigurationUid out of it..
```
curl "https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/devices/ddff93a2-9069-46da-8d26-82f26a420821/summaries" -H "Authorization: Bearer $TOKEN" | jq
```
## or
```
curl "https://www.defenseorchestrator.com/aegis/rest/v1/services/ftd/summaries?q=deviceUid:ddff93a2-9069-46da-8d26-82f26a420821" -H "Authorization: Bearer $TOKEN" | jq 
```
# get the rules of that configuration
```
curl "https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/firewallrules?q=configurationUid:375657bd-da7f-4393-8c0b-9a6cd631572c" -H "Authorization: Bearer $TOKEN" | jq -r '.[].name'
```

# add a rule
```
curl -X POST "https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/firewallrules" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d '
{
    "index": 2,
    "ruleType": "L3",
    "configurationUid": "375657bd-da7f-4393-8c0b-9a6cd631572c",
    "ruleDetails": {
        "@type": "L3RuleDetails",
        "ruleAction": "DENY",
        "remark": "Doron Remark",
        "sourcePorts": [
            {
              "@type": "ObjectReferenceContentWithElements",
              "name": "TCP:80",
              "uid": "2d54af06-84b8-4142-aef0-41a3c4297889",
              "type": "SERVICE_GROUP",
              "elements": [
                "tcp port-object eq 80"
              ]
            }
          ],
          "destinationPorts": [
            {
              "@type": "ObjectReferenceContentWithElements",
              "name": "TCP:80",
              "uid": "2d54af06-84b8-4142-aef0-41a3c4297889",
              "type": "SERVICE_GROUP",
              "elements": [
                "tcp port-object eq 80"
              ]
            }
          ],
          "sourceNetworks": [
            {
              "@type": "ObjectReferenceContentWithElements",
              "name": "10.0.0.224/32",
              "uid": "466e9822-2cc1-4669-bcca-e92d87389da1",
              "type": "NETWORK_GROUP",
              "elements": [
                "10.0.0.224/32"
              ]
            }
          ],
          "destinationNetworks": [
            {
              "@type": "ObjectReferenceContentWithElements",
              "name": "22.22.22.22/32",
              "uid": "d3945fe3-cc1d-4f0b-a83e-aff54b39b28e",
              "type": "NETWORK_GROUP",
              "elements": [
                "22.22.22.22/32"
              ]
            },
            {
              "@type": "ObjectReferenceContentWithElements",
              "name": "IT-Team-Values",
              "uid": "898bfbd0-4845-42be-b382-1e06f964ab05",
              "type": "NETWORK_OBJECT",
              "elements": [
                "9.8.45.12/32"
              ]
            }
          ],
          "syslogEnabled": true
        },
    "name": "Doron"
}
'
```

# Delete rule
```
curl -X DELETE "https://www.defenseorchestrator.com/aegis/rest/v1/services/targets/firewallrules/d67768dc-1aef-43c2-87b2-9753b29e867c" -H "Authorization: Bearer $TOKEN" 
```

