import os
import requests


def upload_config_file(filename, cookies):
    multipart_form_data = {
        'path': '.',
        'file': (filename, open(filename, 'rb'))
    }
    requests.post(url='https://scripts.cisco.com/api/v2/files',
                  files=multipart_form_data,
                  cookies=cookies)

def delete_file(filename, cookies, filetype):
    basename = os.path.basename(filename)
    if filetype is None:
        url = 'https://scripts.cisco.com/api/v2/files/' + basename
    else:
        url = 'https://scripts.cisco.com/api/v2/files/' + basename + '.' + filetype

    requests.delete(url=url, cookies=cookies)
