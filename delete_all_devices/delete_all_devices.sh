#!/bin/sh

#Usage:
#export OAUTH=my_API_token
#bash delete_all_devices.sh 

 
log  () { echo $(date +"[%F %R:%S] ") "$@"; }
fail () { log "$@"; exit 1; }
 
which -s jq || fail "jq must be installed"
[ ${OAUTH} ] || fail "You must specify OAuth token in the \$OAUTH system variable"
 
# validate OAUTH token
API_URL="https://www.defenseorchestrator.com/aegis/rest/v1/services"
curl -s -o /dev/null -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}" || fail "\"${OAUTH}\" is an invalid OAuth token"

DEVICE_URL="${API_URL}/targets/devices"
curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${DEVICE_URL}" | jq -r '.[] | .uid + "," + .name' > allDevices

while read line
do
  IFS=',' read -r DEVICE_UID DEVICE_NAME <<< "$line"
  echo "Deleting: ${DEVICE_NAME}........."
  curl -s -f -H "Authorization: bearer ${OAUTH}" -X DELETE "${DEVICE_URL}/${DEVICE_UID}"
done < allDevices
