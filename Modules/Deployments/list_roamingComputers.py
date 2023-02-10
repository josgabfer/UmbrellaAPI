import datetime 
from dotenv import dotenv_values, find_dotenv
import pandas
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
from ..Auth.getToken import generate_auth_string
from ..Core.getPath import getPath
from ..Core.get import  get_request

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
file_name = f'roaming_computers_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
entry_limit = 100

def get_roamingComputers(token_type):
    try:
        url = "https://api.umbrella.com/deployments/v2/roamingcomputers"
        param = {
            "limit": entry_limit
        }
        fileType = "REPORTFILES"
        path = getPath(fileType)
        sites_json = get_request(token_type, url, param)
        if (sites_json != None):
            sites_list = pandas.DataFrame(sites_json)
            sites_list.to_csv(path + file_name, index=False)
            print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))
