
import os
from . import cdoapi

API_TOKEN=os.getenv('API_TOKEN')
def download_asa_configs(api_token, output_dir):
    cdoapi.get_devices(API_TOKEN)
