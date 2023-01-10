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
file_name = f'policies_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
entry_limit = 100

def get_policies(token_type):
    try:
        policyType = input(colored("Type 'dns' to pull DNS policies or type 'web' to pull WEB policies: ", "blue"))
        if (policyType != 'dns' and policyType != 'web'):
            print(colored("Invalid option", "red"))
            return
        url = "https://api.umbrella.com/deployments/v2/policies"
        param = {
            "limit": entry_limit,
            "type": policyType
        }
        fileType = "REPORTFILES"
        path = getPath(fileType)
        policies_json = get_request(token_type, url, param)
        if (policies_json != None):
            policies_list = pandas.DataFrame(policies_json)
            policies_list.to_csv(path + policyType + "_" + file_name, index=False)
            print(colored(fr"Success! {policyType}_{file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

