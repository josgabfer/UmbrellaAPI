from ..Core.get import get_request
import datetime 
import pandas 
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
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
file_name = f'networks_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
entry_limit = 100

def get_networks(token_type):
    try:
        url = "https://api.umbrella.com/deployments/v2/networks"
        param = {
            "limit": entry_limit
        }
        fileType = "REPORTFILES"
        path = getPath(fileType)
        networks_json = get_request(token_type, url, param)
        if (networks_json != None):
            networks_list = pandas.DataFrame(networks_json)
            networks_list.to_csv(path + file_name, index=False)
            print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

