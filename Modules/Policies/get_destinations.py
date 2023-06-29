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
file_name       : By default the script will use the next Format: destination_list_<year>-<month>-<day>-<hour>-<minute>.csv
entry_limit     : Integer value, here we specify the number of records to be saved in the CSV file."""
entry_limit = 100


def get_destinations(token_type, data):
    try:
        url = f"https://api.umbrella.com/policies/v2/destinationlists/{data[0]}/destinations"
        file_name = f'destination_list_{data[1]}_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'

        print(url)
        param = {
            "limit": entry_limit
        }
        fileType = "REPORTFILES"
        path = getPath(fileType)
        response = get_request(token_type, url, param)
        data = []
        if (response != None):
            dest_list = pandas.DataFrame(response['data'])
            dest_list.to_csv(path + file_name, index=False)
        print(
            colored(f"Success! {file_name} created and stored in {path}", "green"))
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}', 'red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}', 'red'))
