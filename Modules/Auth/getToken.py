import base64
import requests
import os
from requests.models import HTTPError
from requests.auth import HTTPBasicAuth
import http.client as http_client
import logging


http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

ORG = ''
KEY = os.getenv('D_KEY')
SEC = os.getenv('D_SECRET')

def getToken():
    """
        This module will create a new OAUTH2 token for API Queries, more information at:
        https://developer.cisco.com/docs/cloud-security/#!auth-overview
    """
    creds = '{KEY}:{SEC}'.format(KEY=KEY, SEC=SEC)
    URL = 'https://api.umbrella.com/auth/token'
    headers = {
        "Content-Type": "",
        "Accept": "application/json",
        "Authorization": "Basic %s" %credsb64
    }
    try:
        resp = requests.request('POST', URL, headers=headers, data=payload)
        print(resp.text.encode('utf8'))
    except HTTPError as httperr:
        print('Error' + httperr)
    except Exception as e:
        print('Error' + e)

    