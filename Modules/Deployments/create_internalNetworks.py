import datetime
from ..Core.csvToJson import csvToJson
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
from ..Core.post import postItems
import logging
import json
import datetime


http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


# Script variables, must not be changed
date = datetime.datetime.now()
timestamp = date.strftime('_%Y_%m_%d_%H_%M')
lines = ['originId,name,ipAddress,prefixLength,siteName,siteId,networkName,networkId,tunnelName,tunnelId,modifiedAt\n']


"""
User variables - can be changed
logfile         : Specify the path and name of the log file. Default name: create_internal_domains_<year>_<month>_<day>_<hour>_<minute>.csv
tunnels_list    : Location and name of the CSV file that contains the information of the internal domains that will be created in the Umbrella dashboard
"""


def writeInternalNetworkAttributes(response, lines):
    try:

        if response == None or response == '':
            print(colored('None or empty string response detected'))
            exit()
        else:
            data = json.loads((response.text))
        status = response.status_code
        print(colored(data, 'yellow'))

        originId = data['originId'] if status == 200 else 'NA'
        ipAddress = data['ipAddress'] if status == 200 else 'NA'
        prefixLength = data['prefixLength'] if status == 200 else 'NA'
        siteName = data['siteName'] if status == 200 else 'NA'
        createdAt = data['createdAt'] if status == 200 else 'NA'
        name = data['name'] if status == 200 else 'NA'
        siteId = data['siteId'] if status == 200 else 'NA'
        line = str(originId) + ',' + str(ipAddress) + ',' + str(prefixLength) + \
            ',' + siteName + ',' + createdAt + \
            ',' + name + ',' + str(siteId) + '\n'
        lines.append(line)
    except Exception as error:
        print(colored(error, 'red'))
    return lines


def create_internal_networks(token_type):

    logfile = getPath("LOGFILES") + \
        'CREATE_INTERNAL_NETWORKS' + str(timestamp) + ".csv"
    internal_network_list = getPath("CONFILES") + 'internalnetworksinfo.csv'

    url = "https://api.umbrella.com/deployments/v2/internalnetworks"

    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        networks = csvToJson(internal_network_list)
        for network in networks:
            payload = json.dumps({
                "prefixLength": network["prefixLength"],
                "siteId": network["siteId"],
                "ipAddress": network["ipAddress"],
                "name": network["name"]
            })
            print(colored('Adding Internal Network: ' +
                  network['name'], 'green'))
            response = postItems(token_type, url, payload)
            writeInternalNetworkAttributes(response, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)


if __name__ == "__main__":
    create_internal_networks("")
