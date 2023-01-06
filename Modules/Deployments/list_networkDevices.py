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
file_name       : By default the script will use the next Format: networks_list_<year>-<month>-<day>-<hour>-<minute>.csv"""
file_name = f'network_devices_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'

def get_networkDevices(token_type):
    try:
        url = "https://api.umbrella.com/deployments/v2/networkdevices"
        networkDevices_json = get_request(token_type, url)
        if (networkDevices_json != None):
            networkDevices_list = pandas.DataFrame(networkDevices_json)
            fileType = "REPORTFILES"
            path = getPath(fileType)
            networkDevices_list.to_csv(path + file_name, index=False)
            print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))


