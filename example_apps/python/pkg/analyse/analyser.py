import os

from .. import download
import os
from .. import bdb
from ..utils import *
from subprocess import call
import requests
from .. import envutils
import uuid

BDB_SCRIPT = 'ASA_Show_Tech_Parser'


def analyse_configs(api_token, env, output_dir, bdb_username):
    # download ASA configs
    (device_uids, device_names, filenames) = download.download_asa_configs(api_token, env, output_dir)

    cookies = bdb.login(bdb_username)

    report_json_dir = os.path.join(output_dir, 'reports_json')

    if not os.path.exists(report_json_dir):
        print(as_in_progress_msg('Creating analysis output directory (' + report_json_dir + ')...'), end='\r')
        os.makedirs(report_json_dir)
        print(as_done_msg(''))

    i = 0
    report_uid = uuid.uuid4()
    for filename in filenames:
        _analyse_config(filename, report_json_dir, cookies, api_token, env,
                        device_uids[i], device_names[i], report_uid)

    _generate_reports(report_json_dir)
    _create_note(api_token, env, report_uid, BDB_SCRIPT, device_uids)


def _generate_reports(report_json_dir):
    print(as_in_progress_msg('Generating report (' + report_json_dir + ')...'), end='')
    call(['node', '../node/report_generator/report_generator.js', report_json_dir])
    print(as_done_msg(''))


def _analyse_config(filename, report_json_dir, cookies, api_token, env, device_uid, device_name, report_uid):
    print(as_in_progress_msg('Analysing ' + filename + '... '), end='', flush=True)

    bdb.upload_config_file(filename, cookies)

    response = bdb.execute_job_that_takes_file(filename, cookies, BDB_SCRIPT)
    _save_report_to_disk(report_json_dir, filename, response.text)
    _upload_analysis_results_to_cdo(api_token, env, response.text,
                                    device_uid, device_name, report_uid)

    bdb.delete_file(filename, cookies, None)
    bdb.delete_file(filename, cookies, 'json')

    print(as_done_msg(''))


def _save_report_to_disk(report_json_dir, filename, result_data):
    report_file = open(os.path.join(report_json_dir, os.path.basename(filename) + '.json'), 'w')
    report_file.write(result_data)
    report_file.close()


def _upload_analysis_results_to_cdo(api_token, env, result_data, device_uid, device_name, report_uid):
    data = {
        'deviceUid': device_uid,
        'name': device_name,
        'resultData': result_data,
        'reportUid': str(report_uid)
    }

    requests.post(envutils.get_analysis_results_url(env),
                  json=data,
                  headers=envutils.get_headers(api_token))


def _create_note(api_token, env, report_uid, task_name, device_uids):
    print(as_in_progress_msg('Creating CDO notifications...'), end='')
    data = {
        'synopsis': 'Device Analysis task ' + task_name + ' completed',
        'message': 'Analysis performed across ' + str(len(device_uids)) + ' devices',
        'links': [{
            'id': 'config_analysis',
            'params': {
                'reportUid': str(report_uid)
            }
        }]
    }
    requests.post(envutils.get_notes_url(env),
                  json=data,
                  headers=envutils.get_headers(api_token))
    print(as_done_msg(''))
