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
lines = ['id,organizationId,access,isGlobal,name,status,thirdpartyCategoryId,isMspDefault,markedForDeletion,bundleTypeId,meta_destination_count,createdAt,modifiedAt\n']
"""
User variables - can be changed
logfile         : Specify the path and name of the log file. Default name: createTunnelsLog_<year>_<month>_<day>_<hour>_<minute>.csv
tunnels_list    : Location and name of the CSV file that contains the information of the tunnels that will be created in the Umbrella dashboard
"""


def writeDestListAttributes(response, destinations, lines):
    data = json.loads(response.text)
    status = response.status_code
    id = data.get('id', '') if status == 200 else ''
    organizationId = data['organizationId'] if status == 200 else ''
    access = data['access'] if status == 200 else destinations['access']
    isGlobal = data['isGlobal'] if status == 200 else destinations['isGlobal']
    name = data.get('name') if status == 200 else destinations['name']
    thirdpartyCategoryId = data.get(
        'thirdpartyCategoryId') if status == 200 else ''
    bundleTypeId = data.get(
        'bundleTypeId') if status == 200 else destinations['bundleTypeId']
    isMspDefault = data.get('isMspDefault') if status == 200 else ''
    markedForDeletion = data.get(
        'markedForDeletion', '') if status == 200 else ''
    meta_destination_count = data['meta'].get(
        'destinationCount', '') if status == 200 else ''
    modifiedAt = data.get('modifiedAt', '') if status == 200 else ''
    createdAt = data.get('createdAt', '') if status == 200 else ''
    line = str(id) + ',' + str(organizationId) + ',' + str(access) + ',' + str(isGlobal) + ',' + \
        str(name) + ',' + str(status) + ',' + str(thirdpartyCategoryId) + \
        ',' + str(isMspDefault) + ',' + str(markedForDeletion) + \
        ',' + str(bundleTypeId) + ',' + str(meta_destination_count) + \
        ',' + str(modifiedAt) + ',' + str(createdAt) + '\n'
    lines.append(line)
    print(lines)
    return lines


def create_destination_lists(token_type):
    print("entra")
    destination_list = getPath("CONFILES") + 'destlistsinfo.csv'
    logfile = getPath("LOGFILES") + 'CREATE_DESTINATION_LIST' + \
        str(timestamp) + ".csv"
    url = "https://api.umbrella.com/policies/v2/destinationlists"

    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        destlists = csvToJson(destination_list)
        for destinations in destlists:
            isGlobal = False if destinations['isGlobal'] == 'false' or 'False' else True
            payload = json.dumps({
                "bundleTypeId": destinations['bundleTypeId'],
                "access": destinations['access'],
                "name": destinations['name'],
                "destinations": [{
                    'comment': destinations['destinations_comment'],
                    'destination': destinations['destinations_destination'],
                    'type': destinations['destinations_type']
                }],
                "isGlobal": isGlobal
            })
            print(colored('Adding Destination List: ' +
                  destinations['name'], 'green'))

            print(payload)
            response = postItems(token_type, url, payload)
            print(response.text.encode('utf8'))
            writeDestListAttributes(response, destinations, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)
