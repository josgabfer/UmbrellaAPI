import datetime 
from ..Core.csvToJson import csvToJson
from ..Core.post import postItems
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
import logging
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

def create_networks(token_type):

    network_list = getPath("CONFILES") +'networksinfo.csv'
    logfile = getPath("LOGFILES") + 'CREATE_NETWORKS_' + str(timestamp) + ".csv"
    url = "https://api.umbrella.com/deployments/v2/networks"

    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        networks = csvToJson(network_list)
        for network in networks:
            payload = json.dumps({
            "name": network['networkname'],
            "prefixLength": network['prefix'],
            "ipAddress": network['ipaddress'],
            "status": "CLOSED",
            "isDynamic": network['dynamic'] == "True" or network['dynamic'] == "TRUE"
                })
            print(colored('Adding Network: ' + network['domain'],'green'))
            response = postItems(token_type,url, payload)
            writeNetworkAttributes(response, network, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)