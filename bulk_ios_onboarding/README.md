# Purpose
To quickly onboard many IOS devices into a CDO environment.

# To create a new image (developers)
1. From the bulk_ios_onboarding folder, run `docker build -t bulk_ios_onboarding_app .` This will create an executable docker image named `bulk_ios_onboarding_app`
2. Export the image to a tar file `docker save bulk_ios_onboarding_app > bulk_ios_onboarding_app.tar`

# To use a pre-created image (customer)
1. Ensure that you have docker desktop installed. If you do not, see here how you can install it https://www.docker.com/products/docker-desktop
2. Load the app from your terminal using the following command (note, you must be in the bulk_ios_onboarding directory when you run this command)
```
docker load < bulk_ios_onboarding_app.tar
``` 
3. Create a new folder with a file titled `devices.csv` with your device onboarding data (see: Creating Device Info File below). Locate the absolute file path of this new folder.
4. Run the app using this command:
```
docker run -v <absolute_file_path_to_folder_containing_csv_here>:/bulk_ios_onboarding/assets -it bulk_ios_onboarding_app
```
Be sure to provide the absolute path to the folder containing the csv. For instance if you create a file called `devices.csv` that lives in `~/workspace/cdo/devices.csv`, you will want your argument to look like this `-v ~/workspace/cdo/:/bulk_ios_onboarding/assets`. 
5. Respond to the prompts and supervise the onboarding progress. 
  a) note, when asked to supply the SDC name, navigate to the /sdc page in the ui. From there you can see the names of all of your Secure Device Connectors. You may pick the SDC that you want to connect to your devices with. It is recommended to use the "On-Prem" sdc. 

## Creating Device Info File
Create a file that has the following format:
- each row represents a device
- each column represents a field: `name`, `host`, `port`, `username`, `password`, `enablePassword` respectively.
- `enablePassword` field is optional and can be left blank
- csv file should not include header row of column names
- all values will be read in as strings. No quotes are required. If a value contains a comma, you may supply double quotes surrounding the value.
- see `assets/devices.csv.sample` file as a reference example
- important to note this script only supports bulk onboarding of IOS devices

# Troubleshooting
- if you get a response such as `docker: command not recognized`, this means you likely do not have docker correctly installed. 
- if the program cannot read the devices.csv file, that means you are likely not supplying the absolute path correctly. 

