import argparse
import os
from termcolor import colored
from dotenv import dotenv_values
from pathlib import Path
from Modules.Auth.getToken import check_token
from Modules.Deployments.list_roaming_computers import RequestRoamingClients
from datetime import datetime
import json



parser = argparse.ArgumentParser(description='Umbrella API logging interface')
group = parser.add_argument_group('setup')
parser.add_argument('-k','--key', dest='key',metavar='', type=str, help='This value is the key created from your Umbrella Dashboard')
parser.add_argument('-s','--secret', dest='secret', metavar='',type=str, help='This value stores the secret created from your Umbrella Dashboard')
parser.add_argument('-n','--name', dest='name', metavar='',type=str, help='This value represents the new credentials for the connection')
parser.add_argument('-t','--token-type', dest='token_type', metavar='',type=str, help='This argument requires an option to set the token type, either (A: Admin, D: Deployments, P: Policies, R: Reports, X: Custom)')
parser.add_argument('-r','--roaming', action='store_true', help='This argument is to be used with another operator, for example the list operator "-L" to list the roaming computers')



group = parser.add_mutually_exclusive_group()
group.add_argument('-S', '--setup', action='store_true', help='Setup the connection settings, it requires an orgainzation ID (-o), a key (-k) and a secret (-s)')
group.add_argument('-rt', '--request_token', action='store_true', help='Request a new token')
group.add_argument('-L', '--list', action='store_true', help='Request a new token')
group.add_argument('-T', '--test', action='store_true', help='Test')



args = parser.parse_args()

def setupConnectionSettings():
    """
        Calls the API reporting interface to create a token for further use.
        APISettings: Object, stores all the required arguments for a connection to the Umbrella API
        saveConnectionSettings: function in Model.py, this will save the settings in a DB (ConnectionSettings.db) to reuse the settings
    """
    print("Setup Settings")
def check_token_args(token_type):
    if(token_type == 'A' or token_type == 'D' or token_type == 'P' or token_type == 'R' or token_type == 'X'):
        check_token(token_type)
    else:
        print('Invalid option, please use either (A: Admin, D: Deployments, P: Policies, R: Reports, X: Custom)')

def main():
    if args.setup:
        print("setup")
    elif args.test:
        config = dotenv_values("Modules/Auth/.env")
        print(config['X_TOKEN'])
    elif args.request_token:
        print(args.token_type)
        check_token_args(args.token_type)
    elif args.list:
        if args.roaming:
            RequestRoamingClients('X')
    else:
        print(f'Usage: UmbrellaAPI.py [-h] [-o] [-k] [-s] [-n] [-p] [-S | -q | -w | -ct]')

if __name__ =='__main__':
    main()
