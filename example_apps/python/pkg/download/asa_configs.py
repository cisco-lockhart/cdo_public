
import os
from . import cdoapi

API_TOKEN=os.getenv('API_TOKEN')
def download_asa_configs(api_token, output_dir):
    devices = cdoapi.get_devices(API_TOKEN)
    cdoapi.save_device_configs(devices, output_dir)