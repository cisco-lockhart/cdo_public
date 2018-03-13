import os
import requests

BDB_JOBS_URL = 'https://scripts.cisco.com/api/v2/jobs/'

def execute_job_that_takes_file(filename, cookies, job_name):
    basename = os.path.basename(filename)
    job_payload = {
        'input': {
            'session': ['filename'],
            'filename': basename,
            'render_type': 'json',
            'module': '',
            'called_by_other_gw': False
        },
        'dev': False,
        'devAdditionalTasks': []
    }

    return requests.post(url='https://scripts.cisco.com/api/v2/jobs/' + job_name,
                             cookies=cookies,
                             json=job_payload)