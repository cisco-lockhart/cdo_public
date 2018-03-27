import os

from .. import envutils
from .. import download
import os
from .. import bdb
from ..utils import *

def analyse_configs(api_token, env, output_dir, bdb_username):
    base_url = envutils.get_base_url(env)

    # download ASA configs
    filenames = download.download_asa_configs(api_token, env, output_dir)

    cookies = bdb.login(bdb_username)

    report_json_dir = os.path.join(output_dir, 'reports_json')

    if not os.path.exists(report_json_dir):
        print(as_in_progress_msg('Creating analysis output directory (' + report_json_dir + ')...'), end='\r')
        os.makedirs(report_json_dir)
        print(as_done_msg(''))

    for filename in filenames:
        print(as_in_progress_msg('Analysing ' + filename + '... '), end='', flush=True)

        bdb.upload_config_file(filename, cookies)

        response = bdb.execute_job_that_takes_file(filename, cookies, 'ASA_Show_Tech_Parser')
        report_file = open(os.path.join(report_json_dir, os.path.basename(filename) + '.json'), 'w')
        report_file.write(response.text)
        report_file.close()

        bdb.delete_file(filename, cookies, None)
        bdb.delete_file(filename, cookies, 'json')

        print(as_done_msg(''))

