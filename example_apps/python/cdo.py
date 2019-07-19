#!/usr/bin/env python
import argparse
import sys
from pkg.download import asa_configs
from pkg.onboard import onboarder
from pkg.analyse import analyser
from pkg.importers import objectimporter
from pkg.unused import unused_objects
from pkg.jobs import deploy

from pkg.credentials import credentials
from pkg.shadowed import shadows

parser = argparse.ArgumentParser(description='CDO command line')
parser.add_argument("-a", "--api-token", help="The API token to use")
parser.add_argument("-e", "--env", help="The environment to use", choices=['eu', 'us', 'localhost', 'staging'], default='us')

subparsers = parser.add_subparsers(help='Available commands', dest='command')

download_parser = subparsers.add_parser('download')
download_parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/configs')
download_parser.add_argument("-t", "--type", help="The device types to download configs for", choices=['asa'], default='asa')

delete_unused_objects_parser = subparsers.add_parser('delete-unused')
delete_unused_objects_parser.add_argument("-o", "--output-file", help="The output file", default='/tmp/unused-objs.txt')

view_unused_objects_parser = subparsers.add_parser('view-unused')
view_unused_objects_parser.add_argument("-o", "--output-file", help="The output file", default='/tmp/unused-objs.txt')

analyser_parser = subparsers.add_parser('analyse')
analyser_parser.add_argument("-o", "--output-dir", help="The output directory", default='/tmp/configs')
analyser_parser.add_argument("-u", "--username", help="The username to authenticate to BDB")

import_parser = subparsers.add_parser('import')
import_parser.add_argument("-i", "--input-file", help="The input file")

update_credentials_parser = subparsers.add_parser('update-credentials', help='Update ASA credentials')
update_credentials_parser.add_argument("-u", "--username", help="The username to authenticate to BDB")
update_credentials_parser.add_argument("-q", "--query", help='The query to find the devices to update credentials for. E.g.: tags.labels:ctx will find all ASA devices with the label CTX')

shadow_rules_parser = subparsers.add_parser('shadowed', help='Perform operations on shadow rules')
shadow_rules_parser.add_argument("-d", "--delete", help="Delete all shadowed rules", action='store_true')
shadow_rules_parser.add_argument("-q", "--query", help='The query to find the devices to update shadow rules for. '
                                                             'E.g.: tags.labels:ctx will find all ASA devices with the label CTX', default=None)

onboard_parser = subparsers.add_parser('onboard')
onboard_parser.add_argument("-c", "--config-dir", help="The directory holding the configuration files")

deploy_parser = subparsers.add_parser('deploy')
deploy_parser.add_argument("-q", "--query", help='The query to find the devices to deploy.')

args = parser.parse_args()

if args.command == 'download':
    asa_configs.download_asa_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir)
elif args.command == 'view-unused':
    unused_objects.view_unused_objects(api_token=args.api_token, env=args.env, output_file_name = args.output_file)
elif args.command == 'delete-unused':
    unused_objects.delete_unused_objects(api_token=args.api_token, env=args.env, output_file_name = args.output_file)
elif args.command == 'onboard':
    onboarder.upload_asa_configs(api_token=args.api_token, env=args.env, config_dir=args.config_dir)
elif args.command == 'analyse':
    analyser.analyse_configs(api_token=args.api_token, env=args.env, output_dir=args.output_dir, bdb_username=args.username)
elif args.command == 'import':
    objectimporter.import_objects(api_token=args.api_token, env=args.env,csv_file_name=args.input_file)
elif args.command == 'update-credentials':
    credentials.update_credentials(api_token=args.api_token, env=args.env, username=args.username, query=args.query)
elif args.command == 'shadowed':
    shadows.perform_shadowed_action(api_token=args.api_token, env=args.env, query=args.query, delete=args.delete)
elif args.command == 'deploy':
    deploy.deploy_to_devices(api_token=args.api_token, env=args.env, query=args.query)
else:
   sys.stderr.write('Unrecognised command')
