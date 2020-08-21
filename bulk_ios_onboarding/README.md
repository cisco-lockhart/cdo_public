# Purpose
To quickly onboard many IOS devices into a CDO environment.

# Setup
## Step 1: Initialize Virtual Environment
Before running, ensure you have Python3 and Pip
- `python3 --version`
- `pip --version` or `$pip3 --version`

Install VirtualEnv to manage packages for script
- `python3 -m pip install virtualenv`

Create virtual environment
-  `python3 -m venv env`

Activate virtual environment
-  `source env/bin/activate`

You should now be in your virtual environment: where the packages should be
installed to and script should be run from.

Install relevant packages:
- `pip install requests`
- `pip install pybase64`
- `pip install pycryptodome`
- `pip install polling`

## Step 2: Create Device Info File
Create a file in same directory as script called `devices.csv` that has the following format:
- each row represents a device
- each column represents a field: `name`, `host`, `port`, `username`, `password`, `enablePassword` respectively.
- `enablePassword` field is optional and can be left blank
- csv file should not include header row of column names
- all values will be read in as strings, should not supply double or single quotes
- important to note this script only supports bulk onboarding of IOS devices

## Step 3: Create Access Token File
Create a file in same directory as script called `token.txt` that has your authentication token from CDO. You can either reuse a
pre-existing token if you already know it, or refresh/create a new token. 
- Ensure that there is no trailing whitespace or newline in this file

- To get refresh/create new token from CDO:
    - Log in to CDO
    - Navigate to settings page
    - Select `Create` or `Refresh` option
    - A token should be newly generated in a text box. Copy that value and place it in the `token.txt` file. As
    soon as you navigate away from this page, the token will be hidden. 

# Running the Script
Environment should be properly set up now.

By default, this script will execute in US production environment (https://defenseorchestrator.com). 

To execute script in any other valid environment, the envorionment name must be passed in as a `--endpoint` paramater string value. Examples of other valid environments include: 
- https://defenseorchestrator.eu
- https://edge.apj.cdo.cisco.com

To run bulk onboarding script run the following (can include optional endpoint parameter as well): 
- `python3 script.py`
