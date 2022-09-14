import threading
from time import sleep
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import requests
import os
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
from threading import Thread
from ..Auth.getToken import generate_auth_string

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

dotenv_path = Path('../Auth/.env')
load_dotenv()

orgID = os.getenv('ORGID')


def RequestRoamingClients(token_type):
    """ 
        This function will request a list of roaming computers and save it into a csv file for later check
    """
    token = os.getenv(token_type+'_TOKEN')
    print(colored(token),'yellow')
    if token == None:
        print(colored('Token does not exists... Creating a new one', 'red'))
        t = threading.Thread(target=generate_auth_string(token_type))
        t.start()
        sleep(3)
        t.join()
        token = os.getenv(token_type+'_TOKEN')
        if os.getenv(token_type+'_TOKEN') == None:
            print("Error while creating or saving token, please check your code")
    URL="https://api.umbrella.com/deployments/v2/roamingcomputers"
    payload = None
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json"
    }    
    print(colored(f"Contacting the API: {URL}"),'green')
    print("\n")

    try:
        print(colored("Requesting the list of roaming computers"),'green')
        response = requests.request('GET', URL, headers=headers, data = payload)
        if(response.status_code == 401 or response.status_code == 403):
            print("Expired Token, genereting a new one")
            generate_auth_string(token_type)
            t = threading.Thread(target=generate_auth_string(token_type))
            t.start()
            sleep(3)
            t.join()
            RequestRoamingClients(token_type)
        else:
            resp_to_json = response.json()
            clients = pd.DataFrame(resp_to_json)
            clients.to_csv(r'roaming_clients_list.csv', index=False)
            
            

    except HTTPError as httperr:
        print(f'HTPP error occured: {httperr}')
    except Exception as e:
        print(f'HTPP error occured: {e}')
