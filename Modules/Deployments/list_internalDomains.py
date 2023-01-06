from ..Core.get import get_request
import datetime 
import pandas 
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
import json

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
path = ""
file_name = f'internal_domain_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
entry_limit = 100

def getPath():
    with open ("config.json","r") as file:
        config = json.load(file)
    date = datetime.datetime.now()
    timestamp = date.strftime('_%Y_%m_%d_%H_%M')
    path = config['REPORTFILES']['PATH'] + 'LIST_DOMAINS_' + str(timestamp) + ".csv"
    return path

def get_internalDomains(token_type):
    try:
        url = "https://api.umbrella.com/deployments/v2/internaldomains"
        param = {
            "limit": entry_limit
        }
        path = getPath()
        internalDomains_json = get_request(token_type, url, param)
        internalDomains_list = pandas.DataFrame(internalDomains_json)
        internalDomains_list.to_csv(path + file_name, index=False)
        print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

