import argparse

import asa_configs

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--api-token", help="The API token to use")
parser.add_argument("-e", "--env", help="The environment to use", choices=['eu', 'us'], default='us')
parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/asa_configs')

# Add optional arguments to download ASA configs
parser.add_argument("download-asa-configs", help="Download all ASA configs")

args = parser.parse_args()

asa_configs.download_asa_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir)

