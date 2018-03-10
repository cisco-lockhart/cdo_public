# What does this sample do?

This sample allows you to download the configuration files for all of the ASAs
you have onboarded on CDO.

# How do I run it?

- Ensure you have `pip` installed.
- Execute the following commands
  - `pip install virtualenv`
  - `virtualenv venv`
  - `pip install -r requirements.txt`
- Retrieve an API token following the instructions [here](https://docs.defenseorchestrator.com/Tenant_Management/0010_General_Settings#My_Tokens)
- Set the API Token to an environment variable called `$API_TOKEN`
- Execute `python cdo_cmdline.py -a ${API_TOKEN} [-e cdo-environment] [-o output-dir]` where `cdo-environment` 
is either us or eu, depending on which CDO region you retrieved the API token from.

The output directory specified will be populated with a series of config files, one
for each ASA on your CDO deployment, named `name-of-asa-in-cdo.config.txt`.


