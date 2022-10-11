import base64
import requests
import os
from termcolor import colored
from requests.models import HTTPError
from requests.auth import HTTPBasicAuth
import http.client as http_client
import logging
import dotenv
from dotenv import dotenv_values, find_dotenv 



http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
# dotenv.load_dotenv()


def check_token(token_type):
    """
        This module will check if the module exists, it will take a token type
        Token type options: 
            A --> Admin
            D --> Deployments
            P --> Policies
            R --> Reports
            X --> All or custom API 
        If the token exists, it returns the token to the requester
        If the token does not exists, it calls generate token with the token type
    """
    config = dotenv_values(find_dotenv())
    if token_type + '_TOKEN' in config:
        return True
    else:
        return False

def generate_auth_string(token_type):
    """Here we encode the API Secret and Key in base64 format needed for the generate_token() function to request an access token."""
    config = dotenv_values(find_dotenv())
    key = config[token_type + '_KEY']
    secret = config[token_type + '_SECRET']

    auth_string = f"{key}:{secret}"

    message_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_auth = base64_bytes.decode('ascii')
    token_API_Type = token_type + '_' +'TOKEN'

    generate_token(base64_auth, token_API_Type)


def generate_token(base64_auth, token_API_Type):
    """
        This module will create a new OAUTH2 token for API Queries, more information at:
        https://developer.cisco.com/docs/cloud-security/#!auth-overview
    """

    print(colored(f'Refreshing token for token type: {token_API_Type}','yellow'))

    url = "https://api.umbrella.com/auth/v2/token"
    dotenv_file = dotenv.find_dotenv()
    headers = {
        "Authorization": "Basic " + base64_auth
    }
    try:
        response = requests.request("GET", url, headers = headers)
    except HTTPError as httperror:
        print(f'HTPP error occured: {httperror}')
    except Exception as e:
        print(f'An error has occured : {e}')
    token_json = response.json()
    token = token_json.get('access_token')
    print(colored('Token created, saving token to .env file','yellow'))

    dotenv.set_key(dotenv_file,token_API_Type, token)

    return token

