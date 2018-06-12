
import os
from . import cdoapi

API_TOKEN=os.getenv('API_TOKEN')
def download_asa_configs(api_token, output_dir):
    num_devices = cdoapi.get_num_devices(API_TOKEN)
    for offset in range(0, num_devices, 50):
        devices = cdoapi.get_devices(API_TOKEN, offset)
        print ("offset: " + str(offset))
        for device in devices:
            cdoapi.save_device_config(device, output_dir)