import os

from .. import envutils
from .. import download
import requests
import getpass
import sys
import os

def analyse_configs(api_token, env, output_dir, bdb_username):
    base_url = envutils.get_base_url(env)

    # download ASA configs
    filenames = download.download_asa_configs(api_token, env, output_dir)

    print "Analysing files..."
    bdb_password=getpass.getpass(prompt='Enter BDB password: ')
    response = requests.get('https://scripts.cisco.com/api/v2/auth/login', auth=(bdb_username, bdb_password))
    cookies = dict(ObSSOCookie=response.cookies['ObSSOCookie'])

    report_json_dir = os.path.join(output_dir, 'reports_json')
    if not os.path.exists(report_json_dir):
        os.makedirs(report_json_dir)
    for filename in filenames:
        sys.stdout.write('Analysing ' + filename + '...')
        sys.stdout.flush()
        multipart_form_data = {
            'path': '.',
            'file': (filename, open(filename, 'rb'))
        }
        requests.post(url='https://scripts.cisco.com/api/v2/files',
                      files=multipart_form_data,
                      cookies=cookies)

        basename = os.path.basename(filename)
        # https: // scripts.cisco.com / api / v2 / jobs / ASA_Show_Tech_Parser
        job_payload = {
            'input': {
                'session':['filename'],
                'filename': basename,
                'render_type':'json',
                'module': '',
                'called_by_other_gw': False
            },
            'dev': False,
            'devAdditionalTasks': []
        }
        response = requests.post(url='https://scripts.cisco.com/api/v2/jobs/ASA_Show_Tech_Parser',
                      cookies=cookies,
                      json=job_payload)

        report_file = open(os.path.join(report_json_dir, basename + '.json'), 'w')
        report_file.write(response.text)
        report_file.close()

        requests.delete(url='https://scripts.cisco.com/api/v2/files/' + basename + '.json',
                      cookies=cookies)
        requests.delete(url='https://scripts.cisco.com/api/v2/files/' + basename,
                        cookies=cookies)
        print '...done'

