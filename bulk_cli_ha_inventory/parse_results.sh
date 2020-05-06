#!/bin/sh

#Usage:
#bash parse_results.sh results	
 
log  () { echo $(date +"[%F %R:%S] ") "$@"; }
fail () { log "$@"; exit 1; }
 
which -s jq || fail "jq must be installed"
which -s diff || fail "diff must be installed"
[ ${1} ] || fail "${0} <results file name>"
[ -f ${1} ] || fail "results file not found: ${1}"

RESULTS_FILE=${1}
 
cat $RESULTS_FILE | jq 
