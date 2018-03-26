#!/usr/bin/env python
import argparse
import sys
from download import asa_configs

parser = argparse.ArgumentParser(description='CDO command line')
parser.add_argument("-a", "--api-token", help="The API token to use")
parser.add_argument("-e", "--env", help="The environment to use", choices=['eu', 'us', 'localhost'], default='us')

subparsers = parser.add_subparsers(help='Available commands', dest='command')

download_parser = subparsers.add_parser('download')
download_parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/configs')
download_parser.add_argument("-t", "--type", help="The device types to download configs for", choices=['asa'], default='asa')

args = parser.parse_args()

if args.command == 'download':
    asa_configs.download_asa_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir)
else:
   sys.stderr('Unrecognised command')
