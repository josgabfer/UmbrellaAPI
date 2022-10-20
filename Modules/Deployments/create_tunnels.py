from ..Auth.getToken import generate_auth_string
import datetime 
from dotenv import dotenv_values, find_dotenv
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
import logging
import csv
import json


http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


# Script variables, must not be changed
date = datetime.datetime.now()
timestamp = date.strftime('_%Y_%m_%d_%H_%M')
lines = ['tunnelName,deviceType,tunnelID,tunnelkey,umbrellaID,status,error,tunnelCreatedAt\n']

"""
User variables - can be changed
logfile         : Specify the path and name of the log file. Default name: createTunnelsLog_<year>_<month>_<day>_<hour>_<minute>.csv
tunnels_list    : Location and name of the CSV file that contains the information of the tunnels that will be created in the Umbrella dashboard
"""

# logfile = 'C:\\createTunnelsLog'+str(timestamp)+'.csv'
# tunnels_list = 'C:\\tunnelinfo.csv'

def getPath():
    with open ("config.json","r") as file:
        config = json.load(file)
    jsonlogdata = json.dumps(json.dumps(config['LOGFILES']['PATH']))
    cleanlogdata = json.loads(jsonlogdata)
    logfile = cleanlogdata.replace('"','') + 'CREATE_TUNNELS_' + str(timestamp) + ".csv"

    jsonConfData = json.dumps(json.dumps(config['CONFILES']['PATH']))
    cleanConfData = json.loads(jsonConfData)
    confile = cleanConfData.replace('"','') + 'tunnelinfo.csv'
    filesArr = {'LOG':logfile, 'CONF':confile}
    return filesArr


def csvToJson(tunnels_list):
    json_array = []
    with open(tunnels_list, 'r', encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            json_array.append(row)
    json_string = json.dumps(json_array, indent=4)  
    json_data = json.loads(json_string)
    return json_data

def postTunnel(token_type, tunnel):
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    url = "https://api.umbrella.com/deployments/v2/tunnels"
    payload = json.dumps({
        "name": tunnel['tunnelname'],
        "deviceType": tunnel['devicetype'],
        "transport": {
            "protocol": "IPSec"
        },
        "authentication": {
            "type": "PSK",
            "parameters": {
                "idPrefix": tunnel['prefix'],
                "secret": tunnel['key']
            }
        }
    })
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    print(colored(f"Contacting API: {url}", 'green'))
    response = requests.post(url, headers = headers, data = payload)
    try:
        if (response.status_code == 401 or response.status_code == 403):
            print(colored("Token has expired. Generating new token", "red"))
            token = generate_auth_string(token_type)
            return (postTunnel(token_type, tunnel))
        elif (response.status_code == 400 or response.status_code == 409):
            error = response.json()
            print(colored(f"Failed to add tunnel: '{tunnel['tunnelname']}' \nReason: {error.get('error')}", 'red'))
            print("\n")
        elif (response.status_code == 200):
            print (colored(f"Success! Tunnel: {tunnel['tunnelname']} added", 'green'))
            print("\n")
        else:
            print(response.text)
        return response
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

def writeTunnelAttributes(response,tunnel,lines):
    data = json.loads(response.text)
    status = response.status_code
    tunnelName = data.get('name','') if status == 200 else tunnel['tunnelname']
    deviceType = data['client'].get('deviceType','') if status == 200 else tunnel['devicetype']
    tunnelID = data['client']['authentication']['parameters'].get('id',0) if status == 200 else ''
    tunnelkey = tunnel['key']
    umbrellaID = data.get('id',0) if status == 200 else ''
    error = '' if status == 200 else data['error']
    tunnelCreatedAt = data.get('createdAt','') if status == 200 else ''
    line = str(tunnelName) +','+ str(deviceType) +','+ str(tunnelID) +','+ str(tunnelkey) +','+ str(umbrellaID) +','+ str(status) +','+ str(error) +','+ str(tunnelCreatedAt) +'\n'
    lines.append(line)
    return lines

def create_tunnels(token_type):
    files = getPath()
    tunnels_list = files['CONF']
    logfile = files['LOG']
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        tunnels = csvToJson(tunnels_list)
        for tunnel in tunnels:
            response = postTunnel(token_type, tunnel)
            writeTunnelAttributes(response,tunnel,lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)

if __name__  == "__main__":
    create_tunnels("")
