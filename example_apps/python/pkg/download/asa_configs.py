
import os
from . import cdoapi

API_TOKEN=os.getenv('API_TOKEN')

def download_asa_configs(api_token, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    print("Write your code here")
