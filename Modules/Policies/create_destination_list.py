import datetime
from ..Core.csvToJson import csvToJson
from ..Core.post import postItems
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
import logging
import json
import re
import xml.etree.ElementTree as ET


http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


# Script variables, must not be changed
destination_list_xml = getPath("CONFILES") + 'destlistsinfo.xml'
destination_list_csv = getPath("CONFILES") + 'destlistsinfo.csv'
url = "https://api.umbrella.com/policies/v2/destinationlists"
date = datetime.datetime.now()
timestamp = date.strftime('_%Y_%m_%d_%H_%M')
logfile = getPath("LOGFILES") + 'CREATE_DESTINATION_LIST' + \
    str(timestamp) + ".csv"
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


def xml_parser(token_type):
    dest_lists_tree = ET.parse(destination_list_xml)
    category_name = ''
    category_destinations = {}
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        for categories in dest_lists_tree.findall('.//wga_config/prox_acl_custom_categories/prox_acl_custom_category'):
            for category in categories:
                if (category.tag == 'prox_acl_custom_category_name'):
                    category_name = category.text
                if (category.tag == 'prox_acl_custom_category_servers'):
                    for destination in category:
                        if (re.search("^\.", destination.text)):
                            clean_str = re.sub(r"^.", "", destination.text)
                            category_destinations["comment"] = ''
                            category_destinations["destination"] = clean_str
                            category_destinations["type"] = ''
                        else:
                            category_destinations["comment"] = ''
                            category_destinations["destination"] = category.text
                            category_destinations["type"] = ''

            payload = json.dumps({
                "bundleTypeId": 2,
                "access": 'allow',
                "name": category_name,
                "destinations": [category_destinations],
                "isGlobal": False
            })
            response = postItems(token_type, url, payload)
            print(response.text.encode('utf8'))
            writeDestListAttributes(response, dest_lists_tree, lines)
            print(colored(f"Log file created in: {logfile}", "yellow"))
            logFile.writelines(lines)


def csv_parser(token_type):
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        destlists = csvToJson(destination_list_csv)
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

        response = postItems(token_type, url, payload)
        print(response.text.encode('utf8'))
        writeDestListAttributes(response, destinations, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)


def create_destination_lists(token_type, switch):
    if switch == True:
        xml_parser(token_type)
    else:
        csv_parser(token_type)
