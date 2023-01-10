from ..Auth.getToken import generate_auth_string
import datetime 
from dotenv import dotenv_values, find_dotenv
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
from ..Core.post import postItems
from ..Core.csvToJson import csvToJson
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

    logfile = getPath("LOGFILES") + 'CREATE_TUNNELS_' + str(timestamp) + ".csv"
    tunnels_list = getPath("CONFILES") + "tunnelinfo.csv"
    url = "https://api.umbrella.com/deployments/v2/tunnels"
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        tunnels = csvToJson(tunnels_list)
  
        for tunnel in tunnels:
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
            print(colored('Adding Tunnel: ' + tunnel['tunnelname'],'green'))
            response = postItems(token_type, url, payload)
            writeTunnelAttributes(response,tunnel,lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)

if __name__  == "__main__":
    create_tunnels("")
