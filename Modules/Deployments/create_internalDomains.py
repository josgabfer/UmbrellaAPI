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
lines = ['id,domain,description,createdAt,modifiedAt,includeallVAs,includeAllMovileDevices,statusCode,error,message\n']


"""
User variables - can be changed
logfile         : Specify the path and name of the log file. Default name: create_internal_domains_<year>_<month>_<day>_<hour>_<minute>.csv
tunnels_list    : Location and name of the CSV file that contains the information of the internal domains that will be created in the Umbrella dashboard
"""


def writeDomainAttributes(response, lines):
    try:

        if response == None or response == '':
            print(colored('None or empty string response detected'))
            exit()
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
        line = str(id) + ',' + domain + ',' + description + ',' + createdAt + ',' + modifiedAt + ',' + \
            str(includeAllMobileDevices) + ',' + str(includeAllVAs) + \
            ',' + str(statusCode) + ',' + error + ',' + message + '\n'
        lines.append(line)
    except Exception as error:
        print(colored(error, 'red'))
    return lines


def create_domains(token_type):

    logfile = getPath("LOGFILES") + 'CREATE_DOMAINS_' + str(timestamp) + ".csv"
    domain_list = getPath("CONFILES") + 'domaininfo.csv'

    url = "https://api.umbrella.com/deployments/v2/internaldomains"

    with open(str(logfile), 'w', encoding='utf-8') as logFile:
        domains = csvToJson(domain_list)
        print(colored(domains, 'green'))
        for domain in domains:
            payload = json.dumps({
                "description": domain["description"],
                "domain": domain["domain"],
                "includeAllVAs": domain["includeAllMobileDevices"],
                "includeAllMobileDevices": domain["includeAllVAs"]
            })
            print(colored('Adding Domain: ' + domain['domain'], 'green'))
            response = postItems(token_type, url, payload)
            writeDomainAttributes(response, lines)
        print(colored(f"Log file created in: {logfile}", "yellow"))
        logFile.writelines(lines)


if __name__ == "__main__":
    create_domains("")
