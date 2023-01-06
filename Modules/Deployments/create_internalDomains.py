from ..Auth.getToken import generate_auth_string
import datetime 
from dotenv import dotenv_values, find_dotenv
import requests
from requests.models import HTTPError
from termcolor import colored
import http.client as http_client
from ..Core.getPath import getPath
import logging
import csv
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
lines = ['id,domain,description,createdAt,modifiedAt,includeallVAs,includeAllMovileDevices,statusCode,error,message\n']


"""
User variables - can be changed
logfile         : Specify the path and name of the log file. Default name: create_internal_domains_<year>_<month>_<day>_<hour>_<minute>.csv
tunnels_list    : Location and name of the CSV file that contains the information of the internal domains that will be created in the Umbrella dashboard
"""


def csvToJson(network_list):
    json_array = []
    with open(network_list, 'r', encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            json_array.append(row)
    json_string = json.dumps(json_array, indent=4)  
    json_data = json.loads(json_string)
    return json_data

def postDomains(token_type, domain):
    config = dotenv_values(find_dotenv())
    env_token_type = token_type + '_TOKEN'
    token = config.get(env_token_type)

    if (token == None):
        print(colored("Token does not exists. Creating a new token", "red"))
        token = (generate_auth_string(token_type))
    payload = json.dumps({
        "description": domain["description"],
        "domain": domain["domain"],
        "includeAllVAs": domain["includeAllMobileDevices"],
        "includeAllMobileDevices": domain["includeAllVAs"]
    })
    url = "https://api.umbrella.com/deployments/v2/internaldomains"
    headers = {
    'Authorization': 'Bearer ' + token,
    "Content-Type": "application/json"
    }
    print(colored(f"Contacting API: {url}", 'green'))

    response = requests.post(url, headers=headers, data = payload)
    try:
        if (response.status_code == 401 or response.status_code == 403):
            """
            print(colored("Token has expired. Generating new token", "red"))
            token = generate_auth_string(token_type)
            return (postDomain(token_type))
            """
            print(response._content)
            token = generate_auth_string(token_type)
            postDomains(token_type, domain)
        elif (response.status_code == 400 or response.status_code == 409):
            error = response.json()
            print(colored(f"Failed to add domain: \nReason: {error.get('error')}", 'red'))
            print("\n")
            print(response.status_code)
            return response
        elif (response.status_code == 200):
            print (colored(f"Success! Domain added", 'green'))
            print("\n")
            return response
        else:
            print(response.text)
        return response
    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red'))

def writeDomainAttributes(response, lines):
    if response == None or response == '':
        print(colored('None or empty string response detected'))
    else:
        data = json.loads((response.text))
    status = response.status_code
    id = data['id'] if status == 200 else 'NA'
    domain = data['domain'] if status == 200 else 'NA'
    description = data['description'] if status == 200 else 'NA'
    createdAt = data['createdAt'] if status == 200 else 'NA'
    modifiedAt = data['modifiedAt'] if status == 200 else 'NA'
    includeAllVAs = data['includeAllVAs'] if status == 200 else 'NA'
    includeAllMobileDevices = data['includeAllMobileDevices'] if status == 200 else 'NA'
    statusCode = 'NA' if status == 200 else status
    error = 'NA' if status == 200 else data['error']
    message = 'NA' if status == 200 else data['message']
    line = str(id) + ',' + domain + ',' + description + ',' + createdAt + ',' + modifiedAt + ',' + str(includeAllMobileDevices) + ',' + str(includeAllVAs) + ',' + str(statusCode) + ',' + error + ',' + message + '\n'
    lines.append(line)
    return lines

def create_domains(token_type):
    logfile = getPath("LOGFILES") + 'CREATE_DOMAINS_' + str(timestamp) + ".csv"
    domain_list = getPath("CONFILES") + 'domaininfo.csv'

    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        domains = csvToJson(domain_list)
        print(colored(domains,'green'))
        for domain in domains:
            print(colored('Adding Domain: ' + domain['domain'],'green'))
            response = postDomains(token_type, domain)
            writeDomainAttributes(response, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)
    


if __name__  == "__main__":
    create_domains("")
