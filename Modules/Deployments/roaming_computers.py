import datetime 
from dotenv import dotenv_values, find_dotenv
import pandas as pd
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
from ..Auth.getToken import generate_auth_string

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def RequestRoamingClients(token_type):
    """ 
        This function will request a list of roaming computers and save it into a csv file for later check
    """
    config = dotenv_values(find_dotenv())
    token =""
    env_token_type = token_type + '_TOKEN'
    if not env_token_type in config:
        print(colored('Token does not exists... Creating a new one', 'red'))
        token = generate_auth_string(token_type)

    URL="https://api.umbrella.com/deployments/v2/roamingcomputers"
    payload = None
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json"
    }    
    print(colored(f"Contacting the API: {URL}"),'green')
    print("\n")

    try:
        print(colored("Requesting the list of roaming computers","green"))
        response = requests.request('GET', URL, headers=headers, data = payload)
        if(response.status_code == 401 or response.status_code == 403):
            print(colored("Expired Token, genereting a new one","red"))
            token = generate_auth_string(token_type)
            RequestRoamingClients(token_type)
        else:
            print(colored("Success! \nCreating csv file",'green'))
            resp_to_json = response.json()
            clients = pd.DataFrame(resp_to_json)
            file_name = f'roaming_clients_list_{datetime.datetime.now().strftime("%Y-%m-%d")}' + '.csv'
            clients.to_csv(file_name, index=False)
            
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))
    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))
