from ..Auth.getToken import generate_auth_string
from dotenv import dotenv_values, find_dotenv
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
count = 0


def get_request(token_type, url, parameters={}):
    global count
    count += 1
    if (count == 3):
        print(colored(f"\nMaximum attempts to reach {url} exceeded", "red"))
        return
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    print(colored(f"Contacting API: {url}", "green"))
    print("\n")

    try:
        response = requests.get(url, headers=headers, params=parameters)
        if (response.status_code == 401 or response.status_code == 403):
            print(colored(
                f"Failed to connect to {url}. Token might have expired, generating new token\n", "red"))
            token = generate_auth_string(token_type)
            return get_request(token_type, url, parameters)
        elif (response.status_code == 404):
            print(colored("\nError 404 not found", "red"))
        elif (response.status_code == 200):
            print(colored("Get request successfully executed!", "green"))
            print("\n")
            return response.json()
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}', 'red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}', 'red'))
