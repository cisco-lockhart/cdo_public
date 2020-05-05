#!/bin/sh

#Usage:
#export OAUTH=my_API_token
#bash run_bulk_cli.sh devices results	
 
log  () { echo $(date +"[%F %R:%S] ") "$@"; }
fail () { log "$@"; exit 1; }
 
which -s jq || fail "jq must be installed"
which -s diff || fail "diff must be installed"
[ ${OAUTH} ] || fail "You must specify OAuth token in the \$OAUTH system variable"
[ ${1} ] || fail "${0} <input file name> <results file name>"
[ -f ${1} ] || fail "input file not found: ${1}"
[ ${2} ] || fail "${0} <input file name> <results file name>"

DEVICES_FILE=${1}
RESULTS_FILE=${2}
 
# validate OAUTH token
API_URL="https://www.defenseorchestrator.com/aegis/rest/v1/services"
curl -s -o /dev/null -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}" || fail "\"${OAUTH}\" is an invalid OAuth token"


# Initialize the job to no devices
JOB=$(<job.template)

# add device uids to job
DEVICE_URL="${API_URL}/targets/devices"
while read line
do
  IFS=',' read -r DEVICE_UID all_the_rest <<< "$line"
  FAILOVER_MODE=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${DEVICE_URL}/${DEVICE_UID}/configs" | jq -r '.[] | .associated.metadata.failoverMode' )
  if [ $FAILOVER_MODE == "OFF" ] 
  then
    JOB=$(echo "${JOB}" | jq -c --arg UID ${DEVICE_UID} '.objRefs |= . + [ {"uid": $UID,"namespace": "targets", "type": "devices"} ] ')
  fi
done < $DEVICES_FILE

echo ${JOB} > body.json

JOB_URL="${API_URL}/state-machines/jobs"
cat body.json

JOB_ID=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X POST --data @body.json "${JOB_URL}" | jq -r '.uid ' ) 

STATUS=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${JOB_URL}/${JOB_ID}" | jq -r '.overallProgress')
while [ $STATUS == "IN_PROGRESS" ] ||  [ $STATUS == "PENDING" ]
do
  log $STATUS
  sleep 5
  STATUS=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${JOB_URL}/${JOB_ID}" | jq -r '.overallProgress')
done
log $STATUS

curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}/cli/executions?q=jobUid:${JOB_ID}" | jq  > tmpResult

echo "" > tmpResult1
while IFS=',' read -r DEVICE_UID DEVICE_NAME
do
  cat $RESULTS_FILE | jq ".[] | select(.deviceUid == \"${DEVICE_UID}\") | { deviceUid, deviceName: \"${DEVICE_NAME}\", response }" >> tmpResult1
done < $DEVICES_FILE

cat tmpResult1 | jq --slurp '.' > $RESULTS_FILE
