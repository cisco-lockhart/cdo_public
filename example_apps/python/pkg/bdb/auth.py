import getpass
import requests
import sys
from ..utils import *

BDB_BASE_URL = 'https://scripts.cisco.com/api/v2'

BDB_LOGIN_URL = BDB_BASE_URL + '/auth/login'
BDB_LOGOUT_URL = BDB_BASE_URL + '/auth/logout'


def login(bdb_username):
    bdb_password = getpass.getpass(prompt='Enter BDB password: ')
    print(as_in_progress_msg('Authenticating against BDB as ' + bdb_username + '... '), end='', flush=True)
    response = requests.get(BDB_LOGIN_URL, auth=(bdb_username, bdb_password))

    # REALLY? A 201 is a successful response code for a GET? RFC7231 or RFC2616 anyone??
    if response.status_code != 201:
        print(as_error_msg(''))
        sys.exit(-1)

    print(as_done_msg(''))
    return dict(ObSSOCookie=response.cookies['ObSSOCookie'])
