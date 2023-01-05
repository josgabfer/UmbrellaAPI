from ..Core.get import get_request
import datetime 
import pandas 
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
import flatdict as flat

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

"""User variables - can be changed
path            : Location where the file will be saved. Must end with '\\'
file_name       : By default the script will use the next Format: tunnel_list_<year>-<month>-<day>-<hour>-<minute>.csv
delete_columns  : List of columns to be removed from the CSV file. Example: delete_columns = ['client.authentication.parameters.modifiedAt']"""
path = "C:\\Testing\\"
file_name = f'tunnel_list_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}' + '.csv'
delete_columns = []

def get_tunnels(token_type):
    try:
        url = "https://api.umbrella.com/deployments/v2/tunnels"
        param = {
            "status": "DOWN"
        }
        tunnels_json = get_request(token_type, url, param)
        parse_tunnels(tunnels_json)
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red')) 

def parse_tunnels(tunnels_json):
    try:
        for item in range(len(tunnels_json)):
            tunnels_json[item] = flat.FlatDict(tunnels_json[item], '.')
            if delete_columns:
                for delete in delete_columns:
                    tunnels_json[item].pop(delete)
        tunnel_list = pandas.DataFrame(tunnels_json)
        
        tunnel_list.to_csv(path + file_name, index=False)
        
        print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except(AttributeError):
        print(colored("Failed to convert GET response to CSV. Check if the API Path defined in variable 'url' is correct.", "red"))
    except(PermissionError):
        print(colored ("""Failed to save the CSV file. You might be trying to overwrite the file while is already open or the path stored in variable 'path' is invalid.""", "red"))
    except(KeyError):
        print(colored("Failed to delete the columns specified in 'delete_columns'. Make sure there are no typos in the columns' names stored in 'delete_columns'", "red"))
    except:
        print(colored('Unexpected Error.', "red"))
        

if __name__ == "__main__":
    get_tunnels()