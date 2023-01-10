from ..Auth.getToken import generate_auth_string
from dotenv import dotenv_values, find_dotenv
from requests.models import HTTPError
import http.client as http_client
from termcolor import colored
import requests
import logging
import csv
import json
import datetime


http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def postItems(token_type, url, payload = {}):
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    headers = {
    'Authorization': 'Bearer ' + token,
    "Content-Type": "application/json"
    }
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
        print(token)
    print(colored(f"Contacting API: {url}", 'green'))
    response = requests.post(url, headers = headers, data = payload)
    try:
        if (response.status_code == 401 or response.status_code == 403):
            token = generate_auth_string(token_type)
            return postItems(token_type, url, payload)
        elif (response.status_code == 400 or response.status_code == 409):
            error = response.json()
            print(colored(f"Failed to add the items: \nReason: {error.get('error')}", 'red'))
            print("\n")
        elif (response.status_code == 200):
            print (colored(f"Success! Items added", 'green'))
            print("\n")
        else:
            print(response.text)
        return response
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))