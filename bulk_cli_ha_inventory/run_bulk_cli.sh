#!/bin/sh

#Usage:
#export OAUTH=my_API_token
#bash run_bulk_cli.sh devices results	"failover exec standby show version\nshow version"
 
log  () { echo $(date +"[%F %R:%S] ") "$@"; }
fail () { log "$@"; exit 1; }
 
which -s jq || fail "jq must be installed"
which -s diff || fail "diff must be installed"
[ ${OAUTH} ] || fail "You must specify OAuth token in the \$OAUTH system variable"
[ ${1} ] || fail "${0} <input file name> <results file name> <command>"
[ -f ${1} ] || fail "input file not found: ${1}"
[ ${2} ] || fail "${0} <input file name> <results file name> <command>"
[ "${3}" ] || fail "${0} <input file name> <results file name> <command>"

DEVICES_FILE=${1}
RESULTS_FILE=${2}
COMMAND=${3}

# validate OAUTH token
API_URL="https://www.defenseorchestrator.com/aegis/rest/v1/services"
curl -s -o /dev/null -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}" || fail "\"${OAUTH}\" is an invalid OAuth token"

# add device uids to job
JOB=$(<job.template)
while read line
do
  IFS=',' read -r DEVICE_UID all_the_rest <<< "$line"
  JOB=$(echo "${JOB}" | jq -c --arg UID ${DEVICE_UID} '.objRefs |= . + [ {"uid": $UID,"namespace": "targets", "type": "devices"} ] ')
done < $DEVICES_FILE

# add command to job
# COMMAND="failover exec standby show versions"
JOB=$(echo "${JOB}" | jq --arg cmd "${COMMAND}" '. + {jobContext: {command : ($cmd)}} ')

# run the job
echo ${JOB} > body.json
cat body.json | jq
JOB_URL="${API_URL}/state-machines/jobs"
JOB_ID=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X POST --data @body.json "${JOB_URL}" | jq -r '.uid ' ) 

STATUS=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${JOB_URL}/${JOB_ID}" | jq -r '.overallProgress')
while [ $STATUS == "IN_PROGRESS" ] ||  [ $STATUS == "PENDING" ]
do
  log $STATUS
  sleep 5
  STATUS=$(curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${JOB_URL}/${JOB_ID}" | jq -r '.overallProgress')
done
log $STATUS

curl -s -f -H "Content-Type: application/json" -H "Authorization: bearer ${OAUTH}" -X GET "${API_URL}/cli/executions?q=jobUid:${JOB_ID}" | jq '.[] |  { deviceUid, deviceName, executionState, errorMsg, response }' | jq --slurp '.' > $RESULTS_FILE

