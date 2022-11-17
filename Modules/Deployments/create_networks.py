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
lines = ['networkname, ipaddress, prefix, dynamic, originID, status, error, message, networkCreatedAt\n']

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
    logfile = config['LOGFILES']['PATH'] + 'CREATE_NETWORKS_' + str(timestamp) + ".csv"
    confile = config['CONFILES']['PATH'] + 'networksinfo.csv'
    return {
        'LOG': logfile,
        'CONF': confile
    }

def csvToJson(network_list):
    json_array = []
    with open(network_list, 'r', encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            json_array.append(row)
    json_string = json.dumps(json_array, indent=4)  
    json_data = json.loads(json_string)
    return json_data

def postNetwork(token_type, network):
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)
    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    url = "https://api.umbrella.com/deployments/v2/networks"
    payload = json.dumps({
        "name": network['networkname'],
        "prefixLength": network['prefix'],
        "ipAddress": network['ipaddress'],
        "status": "CLOSED",
        "isDynamic": network['dynamic'] == "True" or network['dynamic'] == "TRUE"
    })
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    print(colored(f"Contacting API: {url}", 'green'))
    response = requests.post(url, headers = headers, data = payload)
    try:
        if (response.status_code == 401 or response.status_code == 403):
            """
            print(colored("Token has expired. Generating new token", "red"))
            token = generate_auth_string(token_type)
            return (postTunnel(token_type))
            """
            print(response._content)
        elif (response.status_code == 400 or response.status_code == 409):
            error = response.json()
            print(colored(f"Failed to add tunnel: \nReason: {error.get('error')}", 'red'))
            print("\n")
        elif (response.status_code == 200):
            print (colored(f"Success! Network added", 'green'))
            print("\n")
        else:
            print(response.text)
        return response
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

def writeNetworkAttributes(response, network, lines):
    data = json.loads(response.text)
    status = response.status_code
    networkName = data.get('name','') if status == 200 else network['networkname']
    ipAddress = data['ipAddress'] if status == 200 else network['ipaddress']
    prefixLength = data['prefixLength'] if status == 200 else network['prefix']
    isDynamic = data['isDynamic'] if status == 200 else network['dynamic']
    originID = data.get('originId',0) if status == 200 else ''
    error = '' if status == 200 else data['error']
    message = data.get('message') 
    networkCreatedAt = data.get('createdAt','') if status == 200 else ''
    line = str(networkName) +','+ str(ipAddress) +','+ str(prefixLength) +','+ str(isDynamic) +','+ str(originID) +','+ str(status) +','+ str(error) + ','+ str(message) + ',' + str(networkCreatedAt) +'\n'
    lines.append(line)
    return lines
#lines = ['networkname, ipaddress, prefix, dynamic, originID, status, error, networkCreatedAt\n']

def create_networks(token_type):
    files = getPath()
    network_list = files['CONF'] 
    logfile = files['LOG']
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        networks = csvToJson(network_list)
        for network in networks:
            #postNetwork(token_type, network)
            response = postNetwork(token_type, network)
            writeNetworkAttributes(response, network, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)