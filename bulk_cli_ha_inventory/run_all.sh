#!/bin/sh


OAUTH=my_API_token
./fetch_ha_devices.sh > devices
./run_bulk_cli.sh devices results "failover exec standby show version\nshow version"
./parse_results.sh results

