
import os
from . import cdoapi

API_TOKEN=os.getenv('API_TOKEN')
def download_asa_configs(api_token, output_dir):
    cdoapi.get_num_devices(API_TOKEN)
    devices = cdoapi.get_devices(API_TOKEN)
    for device in devices:
        cdoapi.save_device_config(device, output_dir)