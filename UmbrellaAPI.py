import argparse
import os
import json

from ConnectionModules.Create_Token import request_Token
from API_Modules.Umbrella.Monitoring.ReportActivity import ReportActivitySearch, ReportDNSSumary
from API_Modules.Umbrella.Management.management import RequestIdentities, RequestRoamingClients
# from API_Modules.Umbrella.Monitoring.tunnelMonitoring import CheckTunnelState
from datetime import datetime

os.environ["TOKEN"] = "TEST"



parser = argparse.ArgumentParser(description='Umbrella API logging interface')
group = parser.add_argument_group('setup')
parser.add_argument('-o','--oid', dest='orgid', metavar='',type=str, help='oid is the organization ID, this value can be found in your umbrella dashboard URL')
parser.add_argument('-k','--key', dest='key',metavar='', type=str, help='This value is the key created from your Umbrella Dashboard')
parser.add_argument('-s','--secret', dest='secret', metavar='',type=str, help='This value stores the secret created from your Umbrella Dashboard')
parser.add_argument('-n','--name', dest='name', metavar='',type=str, help='This value represents the new credentials for the connection')
parser.add_argument('-p','--path', dest='path', metavar='',type=str, help='This value instructs the program where to save the Database in your OS, for example Windows: C:\\\\path\\\\to\\\\ ---- Unix/Mac: sqlite:////absolute/path/to/foo.db')
parser.add_argument('-ar','--activity', dest='activity', metavar='',type=str, help='This argument will tell the program to query the Activity Report in Cisco Umbrella')


group = parser.add_mutually_exclusive_group()
group.add_argument('-S', '--setup', action='store_true', help='Setup the connection settings, it requires an orgainzation ID (-o), a key (-k) and a secret (-s)')
group.add_argument('-rt', '--requestToken', action='store_true', help='Request a new token')
group.add_argument('-ra', '--requestActivity', action='store_true', help='Check Report Activity')
group.add_argument('-rs', '--requestSummary', action='store_true', help='Check DNS Summary information')
group.add_argument('-ri', '--requestIdentities', action='store_true', help='Check Identities Summary information')
group.add_argument('-rr', '--requestroamingclients', action='store_true', help='Check Identities Summary information')
# group.add_argument('-ri', '--requestIdentities', action='store_true', help='Check Identities Summary information')
group.add_argument('-q', '--query', action='store_true', help='Query the Umbrella\'s API')
group.add_argument('-ts', '--TunnelState', action='store_true', help='QThis value tells the program to check the current state of the network tunnels')
group.add_argument('-w', '--write', action='store_true', help='This option will write the information within the DB into an external file (currently in clear text)')


args = parser.parse_args()

def setupConnectionSettings():
    """
    Calls the API reporting interface to create a token for further use.
        APISettings: Object, stores all the required arguments for a connection to the Umbrella API
        saveConnectionSettings: function in Model.py, this will save the settings in a DB (ConnectionSettings.db) to reuse the settings
    """
    print("Setup Settings")


def main():
    if args.setup:
        # requestNetworkIdentities()
        print("setup")
    elif args.requestActivity:
        ReportActivitySearch()
    elif args.requestSummary:
        ReportDNSSumary()
    elif args.requestIdentities:
        RequestIdentities()
    elif args.requestroamingclients:
        # print("Roaming Clients")
        RequestRoamingClients()
    else:
        print(f'Usage: UmbrellaAPI.py [-h] [-o] [-k] [-s] [-n] [-p] [-S | -q | -w | -ct]')

if __name__ =='__main__':
    main()
