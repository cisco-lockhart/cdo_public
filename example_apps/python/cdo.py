#!/usr/bin/env python
import argparse
import sys
from pkg.download import asa_configs
from pkg.analyse import analyser
from pkg.importers import objectimporter

parser = argparse.ArgumentParser(description='CDO command line')
parser.add_argument("-a", "--api-token", help="The API token to use")
parser.add_argument("-e", "--env", help="The environment to use", choices=['eu', 'us', 'localhost', 'staging'], default='us')

subparsers = parser.add_subparsers(help='Available commands', dest='command')

download_parser = subparsers.add_parser('download')
download_parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/configs')
download_parser.add_argument("-t", "--type", help="The device types to download configs for", choices=['asa'], default='asa')

analyser_parser = subparsers.add_parser('analyse')
analyser_parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/configs')
analyser_parser.add_argument("-u", "--username", help="The username to authenticate to BDB")

import_parser = subparsers.add_parser('import')
import_parser.add_argument("-i", "--input-file", help="The input file")
args = parser.parse_args()


if args.command == 'download':
    asa_configs.download_asa_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir)
elif args.command == 'analyse':
    analyser.analyse_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir, bdb_username=args.username)
elif args.command == 'import':
    objectimporter.import_objects(api_token=args.api_token,env=args.env,csv_file_name=args.input_file)
else:
   sys.stderr('Unrecognised command')
