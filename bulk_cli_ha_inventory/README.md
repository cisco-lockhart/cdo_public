# Create an inventory of Standby devices

Problem: CDO onboards an HA pair as a single device. Metadata shown (serial number, versions, etc.) is for the primary device. I wish to create an inventory of these "hidden" standby ASAs out there.

Solution: run a bulk CLI "failover exec standby show ***" on all HA devices

In this directory I have everything I need to succeed in this, hopefully in separate, reusable scripts:
1. Fetch all HA ASAs, run a bulk CLI on all, get results

1. `./fetch_ha_devices.sh > devices` -- will fetch all HA ASAs and will put them in a CSV file `devices`, containing `uid,name`
2. `./run_bulk_cli.sh devices results` -- will create a job across all devices in the `devices` input file and create a `results` file with a json contains:
2.1 deviceName
2.2 deviceUid
2.3 results
3. Parsing results... can be painful...
