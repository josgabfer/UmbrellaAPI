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
dest_lists_info_col = ['bundleTypeId,access,name\n']
dest_list_det_col = ['comment,destination,type\n']
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


def xml_parser():
    dest_lists_tree = ET.parse(destination_list_xml)
    destination_list_details_csv = ''

    dest_list_info_details = []
    for categories in dest_lists_tree.findall('.//wga_config/prox_acl_custom_categories/prox_acl_custom_category'):
        for category in categories:
            if (category.tag == 'prox_acl_custom_category_name'):
                if (re.search(" ", category.text)):
                    clean_str = re.sub(r" ", "_", category.text)
                    destination_list_details_csv = getPath(
                        "CONFILES") + 'destinations_' + clean_str + '.csv'
                    dest_lists_info_col.append(
                        '2' + ',' + 'allow' + ',' + clean_str + '\n')
                else:
                    destination_list_details_csv = getPath(
                        "CONFILES") + 'destinations_' + category.text + '.csv'
                    dest_lists_info_col.append(
                        '2' + ',' + 'allow' + ',' + category.text + '\n')
                dest_list_info_details = []
            if (category.tag == 'prox_acl_custom_category_servers'):
                with open(str(destination_list_details_csv), 'w', encoding='utf-8') as destination_list:
                    for destination in category:
                        if (re.search("^\.", destination.text)):
                            clean_str = re.sub(r"^.", "", destination.text)
                            dest_list_info_details.append(
                                'WAS_Migration' + ',' + clean_str + ',' + 'DOMAIN' + '\n')
                        else:
                            dest_list_info_details.append(
                                'WAS_Migration' + ',' + destination.text + ',' + 'DOMAIN' + '\n')
                    dest_list_info_details = list(set(dest_list_info_details))
                    dest_list_info_details.insert(
                        0, 'comment,destination,type\n')
                    destination_list.writelines(dest_list_info_details)
                    print(colored('Added list of destinations: ' +
                          str(dest_list_info_details), 'green'))

    with open(str(destination_list_csv), 'w', encoding='utf-8') as destination_list_info:
        destination_list_info.writelines(dest_lists_info_col)
        print(colored('Created destlistinfo.csv succesfully', 'green'))
        print(colored('Please check the files destlistinfo.csv and destinations '))


def csv_parser(token_type):
    files_path = getPath("CONFILES")
    destination_list_details_csv = ''
    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        list_of_dest_lists = csvToJson(destination_list_csv)
        for current_destination_info in list_of_dest_lists:
            destination_list_array = []
            bundleTypeId = current_destination_info['bundleTypeId']
            access = current_destination_info['access']
            name = current_destination_info['name']
            destination_list_details = csvToJson(files_path + 'destinations_' +
                                                 destination_list_details_csv + name + '.csv')
            for destination in destination_list_details:
                print(destination)
                print(destination)
                destination_list_array.append(destination)
                payload = json.dumps({
                    "bundleTypeId": bundleTypeId,
                    "access": access,
                    "name": name,
                    "destinations": destination_list_array,
                    "isGlobal": False
                })
            print(colored('Adding Destination List: ' +
                          name, 'green'))
            print(payload)
            response = postItems(token_type, url, payload)
            print(response.text.encode('utf8'))
            writeDestListAttributes(response, destination_list_array, lines)
            print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)


def create_destination_lists(token_type, switch):
    if switch == True:
        xml_parser()
    else:
        csv_parser(token_type)
