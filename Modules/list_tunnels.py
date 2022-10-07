from Auth.getToken import generate_auth_string
import datetime 
from dotenv import dotenv_values, find_dotenv
import pandas 
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
import flatdict as flat

"""User variables - can be changed
path_name: Here you can specify the path and name of the CSV file that we will use to save the output from the GET request.
delete_columns: Here you can specify the name of the columns that you don't want to appear in the CSV file, for example: delete_columns = ['client.authentication.parameters.modifiedAt']"""
path = "C:\\Users\\dgonzal4\\OneDrive - Cisco\\Desktop\\Python\\"
delete_columns = []

def parse_tunnels(tunnels_json):
    try:
        for item in range(len(tunnels_json)):
            tunnels_json[item] = flat.FlatDict(tunnels_json[item], '.')
            if delete_columns:
                for delete in delete_columns:
                    tunnels_json[item].pop(delete)
        tunnel_list = pandas.DataFrame(tunnels_json)
        file_name = f'tunnel_list_{datetime.datetime.now().strftime("%Y-%m-%d")}' + '.csv'
        tunnel_list.to_csv(path + file_name, index=False)
        
        print(colored(f"Success! {file_name} created and stored in {path}", "green"))
    except(AttributeError):
        print(colored("Failed to convert GET response to CSV. Check if the API Path defined in variable 'url' is correct.", "red"))
    except(PermissionError):
        print(colored ("""Failed to save the CSV file. Check if a valid path and file name were saved in the variable 'path_name'.
Make sure you don't have an opened CSV file with the same name in the same path defined in the variable 'path_name'.""", "red"))
    except(KeyError):
        print(colored("Failed to delete the columns specified in 'delete_columns'. Make sure there are no typos in the columns' names stored in 'delete_columns'", "red"))
    except:
        print(colored('Unexpected Error.', "red"))
        
    

def get_tunnels(token_type):

    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    url = "https://api.umbrella.com/deployments/v2/tunnels"
    payload = None
    headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
    print(colored(f"Contacting API: {url}"), 'green')
    print("\n")

    try:
        print((colored("Gathering tunnels information", "green")))
        response = requests.get(url, headers = headers)
        if (response.status_code == 401 or response.status_code == 403):
            print(colored("Token has expired. Generating new token", "red"))
            token = generate_auth_string(token_type)
            get_tunnels(token_type)
        elif (response.status_code == 200):
            tunnels_json = response.json()
            parse_tunnels(tunnels_json)

    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

"""
def get_tunnels ():
    #In this function we will send a GET request to get a list of all the tunnels listed in the Umbrella dashboard.
    #First, we call the authentication module to retrieve the access token that will be used in the GET request.
    #If the response status code is 401 or 403 it means that the token is expired or invalid. We generate a new token and call the function get_tunnels() again.
    #If the response is successful (status code 200) then we use the flatdict package to flat the dictionary stored in tunnels_json. Here we check as well if there are any columns to be removed from the final CSV file.
    try:
        token = authentication.retrieve_token()
        url = "https://api.umbrella.com/deployments/v2/tunnels"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        response = requests.request("GET", url, headers = headers)
        if (response.status_code == 401 or response.status_code == 403):
            authentication.generate_token()
            return get_tunnels()
        elif response.status_code == 200:
            tunnels_json = response.json()
            for item in range(len(tunnels_json)):
                tunnels_json[item] = flat.FlatDict(tunnels_json[item], '.')
                if delete_columns:
                    for delete in delete_columns:
                        tunnels_json[item].pop(delete)
            return pandas.DataFrame(tunnels_json)
    except:
        print('GET request failed')
"""
if (__name__ == "__main__"):
    get_tunnels("X")