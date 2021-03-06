#!/bin/bash

#Usage:
#export OAUTH=my_API_token
#bash cdo.update.overrides input.csv doit

# log  () { echo $(date +"[%F %R:%S] ") "$@"; }
log() { echo "$@"; }
failexit() {
  log "failure: $@"
  exit 1
}
fail() { log "failure: $@"; }

which -s jq || fail "jq must be installed"
[ ${OAUTH} ] || fail "You must specify OAuth token in the \$OAUTH system variable"
[ ${1} ] || fail "${0} <input CSV file name> [doit]"
[ -f ${1} ] || fail "input file not found: ${1}"

# validate OAUTH token
API_URL="https://www.defenseorchestrator.com/aegis/rest/v1/services"
curl -s -o /dev/null -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}" || failexit "\"${OAUTH}\" is an invalid OAuth token"

[ ${2} ] || log "****** DRY RUN **********"

while read -r line; do
  # eliminate bad bad bad characters. And adding some padded comas to avoid other issues
  line=${line//[$'\t\r\n ']/},,,,,,
  IFS=',' read -r -a array <<<"$line"
  DEVICE_NAME="${array[0]}"
  OBJECT_NAME="${array[1]}"
  NEW_VALUE="${array[2]}"
  NEW_DEST="${array[3]}"

  log "processing line: ${DEVICE_NAME} ${OBJECT_NAME} ${NEW_VALUE}"

  # handle range values. e.g. 10.10.238.16-10.10.238.17
  NEW_SOURCE=$(echo "${NEW_VALUE}" | cut -d '-' -f 1)
  NEW_DEST=$(echo "${NEW_VALUE}" | cut -d '-' -f 2)
  # if no range, then both values are same, have NEW_DEST be null, otherwise quote it, I won't add quotes in the concat
  if [ "${NEW_DEST}" == "${NEW_SOURCE}" ]; then
    NEW_DEST=null
  else
    NEW_DEST="\"${NEW_DEST}\""
  fi

  DEVICE_URL="${API_URL}/targets/devices"
  unset DEVICE_UID
  DEVICE_UID=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${DEVICE_URL}?q=name:${DEVICE_NAME}" | jq -r '.[0].uid')
  if [ "x${DEVICE_UID}x" == "xx" ] || [ "x${DEVICE_UID}" == "xnull" ]; then
    log "   could not find device by name ${DEVICE_NAME}"
    continue
  fi

  log "   (with device UID): ${DEVICE_NAME} ${DEVICE_UID} ${OBJECT_NAME} ${NEW_SOURCE} ${NEW_DEST}"

  # find and retrieve the object
  OBJECT_URL="${API_URL}/targets/objects"
  OBJECT_SEARCH_URL="${OBJECT_URL}?q=name:${OBJECT_NAME}%20AND%20issueType:SHARED%20AND%20references.uid:${DEVICE_UID}"
  # curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${OBJECT_SEARCH_URL}" | jq
  unset OBJECT_UID
  unset RESPONSE
  unset CURRENT_OVERRIDES_EXCLUDING_DEVICE

  RESPONSE=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${OBJECT_SEARCH_URL}" | jq -r '.[0]')
  OBJECT_UID=$(echo ${RESPONSE} | jq -r '.uid')

  if [ "x${OBJECT_UID}x" == "xx" ] || [ "x${OBJECT_UID}" == "xnull" ]; then
    log "   could not find object by name ${OBJECT_NAME}"
    continue
  fi

  log "   (with object UID): ${DEVICE_NAME} ${DEVICE_UID} ${OBJECT_NAME} ${OBJECT_UID} ${NEW_SOURCE} ${NEW_DEST}"
  CURRENT_OVERRIDES_EXCLUDING_DEVICE=$(echo ${RESPONSE} | jq -r --arg DEVICE_UID "${DEVICE_UID}" '.overrides | map(select(.reference | .uid == $DEVICE_UID | not))')
  log "   Existing overrides ${CURRENT_OVERRIDES_EXCLUDING_DEVICE}"
  NEW_OVERRIDE="{ \"reference\": {\"uid\": \"${DEVICE_UID}\", \"@type\": \"ObjectReferenceForAtomicOperations\", \"namespace\": \"targets\", \"type\": \"devices\"}, \"overrideContents\" : [ { \"@type\": \"NetworkContent\", \"sourceElement\": \"${NEW_SOURCE}\", \"destinationElement\": ${NEW_DEST}, \"wildcardMaskElement\": null } ] }"

  echo $CURRENT_OVERRIDES_EXCLUDING_DEVICE | jq --argjson NEW_OVERRIDE "${NEW_OVERRIDE}" '. + [$NEW_OVERRIDE] | { overrides: . }' > body.json
  log "   PUT body: "`cat body.json`

  if [ "${2}" == "doit" ]; then
    log "   executing PUT......."
    curl -s -o output.txt -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X PUT --data @body.json "${OBJECT_URL}/${OBJECT_UID}" || fail "update object ${OBJECT_NAME} to ${NEW_SOURCE},${NEW_DEST} on device ${DEVICE_NAME} "
  fi

done <${1}
exit
