from operator import index
from ..Auth.getToken import generate_auth_string
import datetime 
from dotenv import dotenv_values, find_dotenv
import pandas 
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

"""User variables - can be changed
path            : Location where the file will be saved. Must end with '\\'
file_name       : By default the script will use the next Format: networks_list_<year>-<month>-<day>-<hour>-<minute>.csv
entry_limit     : Integer value, here we specify the number of records to be saved in the CSV file."""
path = "C:\\Testing\\"
file_name = f'virtual_appliances_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
entry_limit = 100

def get_vas(token_type):
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    url = "https://api.umbrella.com/deployments/v2/virtualappliances"
    payload = None
    parameters = {
        "limit" : entry_limit
    }
    headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
    print(colored(f"Contacting API: {url}"), 'green')
    print("\n")

    try:
        print((colored("Gathering virtual appliances information", "green")))
        response = requests.get(url, headers = headers, params=parameters)
        if (response.status_code == 401 or response.status_code == 403):
            print(colored("Token has expired. Generating new token", "red"))
            token = generate_auth_string(token_type)
            get_vas(token_type)
        elif (response.status_code == 200):
            vas_json = response.json()
            vas_list = pandas.DataFrame(vas_json)
            vas_list.to_csv(path + file_name, index=False)
            print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

