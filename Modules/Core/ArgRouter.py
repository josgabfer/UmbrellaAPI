from pathlib import Path
from Modules.Auth.getToken import check_token
from datetime import datetime
from dotenv import dotenv_values
from getpass import getpass
import hashlib
import dotenv
import json
from termcolor import colored
from Modules.Deployments.list_tunnels import get_tunnels
from Modules.Deployments.list_internalDomains import get_internalDomains
from Modules.Deployments.list_networks import get_networks
from Modules.Deployments.list_sites import get_sites
from Modules.Deployments.list_internalNetworks import get_internalNetworks
from Modules.Deployments.list_networkDevices import get_networkDevices
from Modules.Deployments.list_va import get_vas
from Modules.Deployments.create_tunnels import create_tunnels
from Modules.Deployments.create_internalDomains import create_domains
from Modules.Deployments.create_internalNetworks import create_internal_networks
from Modules.Deployments.list_roamingComputers import get_roamingComputers
from Modules.Deployments.list_policies import get_policies
from Modules.Policies.create_destination_list import create_destination_lists


def setPassword():
    """Creates a hash if password protected profiles are created"""
    count = 0
    salt = "IamyourFath3r"
    p = getpass('Enter your password:\n')
    p2 = getpass('Re-enter your password:\n')
    if not p == p2:
        print(colored('Passwords do not match, please try again\n', 'red'))
        count = + 1
        if count == 5:
            print(colored('Exiting...', 'red'))
            exit()
        setPassword()
    else:
        password = salt + p
        hashed = hashlib.md5(password.encode())
        return hashed


def checkPassword(profile):
    """Checks if the profile entered uses a password or not, if it has a password
    the user will need to enter the password and the system will check if is correct or not"""
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    config = dotenv_values()

    profile = profile + '_PASSW'

    if profile in config:
        p = getpass('Enter the password \n')
        salt = "IamyourFath3r"
        password = salt + p
        hashed = hashlib.md5(password.encode())

        if hashed.hexdigest() == config[profile]:
            return True
        else:
            return False
    else:
        return True


def setup(args):
    """Creates the config.json file.
    This file contains settings like the path to save the reports created by the API, or API name profiles."""

    dotenv_file = dotenv.find_dotenv()
    if (dotenv_file == ""):
        print(colored("No .env file found. Creating new .env file.", "yellow"))
        with open(".env", 'w') as file:
            file.write("#.env variables\n")
        dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    if args.config:
        config = dotenv_values()
        res = [val for key, val in config.items() if 'PROFILE' in key]
        print(colored('+++++++Profiles+++++++', 'green'))
        for val in res:
            print('Profile: ', val)
        res = [val for key, val in config.items() if 'PATH' in key]
        print(colored('+++++++Paths+++++++', 'green'))

        for val in res:
            print('Path: ', val)

    if not args.name:
        if args.path:
            dotenv.set_key(dotenv_file, 'PATH', args.path)
    else:
        question = input(
            "Would you like to protect this profile with a password?\n Y?\n N?\n")
        if question == 'Y' or question == 'y':
            key_name = args.name + '_KEY'
            secret_name = args.name + '_SECRET'
            profile_name = 'PROFILE_' + args.name
            creds_name = args.name + '_PASSW'
            passw = setPassword()
            dotenv.set_key(dotenv_file, profile_name, args.name)
            dotenv.set_key(dotenv_file, key_name, args.key)
            dotenv.set_key(dotenv_file, secret_name, args.secret)
            dotenv.set_key(dotenv_file, creds_name, passw.hexdigest())
            print(colored('Succesfully created a new protected profile', 'green'))
        else:
            key_name = args.name + '_KEY'
            secret_name = args.name + '_SECRET'
            profile_name = 'PROFILE_' + args.name

            dotenv.set_key(dotenv_file, profile_name, args.name)
            dotenv.set_key(dotenv_file, key_name, args.key)
            dotenv.set_key(dotenv_file, secret_name, args.secret)
            print(colored('Succesfully created a new profile', 'green'))


def check_profile(profile):
    """This function will check if the profile exists or not, depending on what is entered by the user"""
    dotenv.load_dotenv()
    config = dotenv_values()

    if profile in config.values():
        return True
    else:
        return False


def argument_router(args):
    """This function will read the arguments entered, and redirect to any given module as required"""
    if not args.setup:
        if args.profile == None:
            with open("config.json", "r") as file:
                config = json.load(file)
            jsondumpsprofile = json.dumps(
                json.dumps(config['DEFAULT_PROFILE']))
            jsonloadprofile = json.loads(jsondumpsprofile)
            cleandata = jsonloadprofile.replace('"', '')
            args.profile = cleandata
        if not checkPassword(args.profile):
            print(colored('Wrong password, please try again', 'red'))
            exit()

    if args.create:
        if args.auth:
            print(colored('Test Create Authentication API', 'yellow'))
        if args.admin:
            print(colored('Test Create Admin API', 'yellow'))
        if args.deployments:
            if args.tunnel:
                create_tunnels(args.profile)
            if args.domains:
                create_domains(args.profile)
            if args.internalNetworks:
                create_internal_networks(args.profile)
        if args.policies:
            create_destination_lists(args.profile)
        if args.reports:
            print(colored('Test Create Reports API', 'yellow'))
    elif args.list:
        if args.auth:
            print(colored('Test List Authentication API', 'yellow'))
        if args.admin:
            print(colored('Test List Admin API', 'yellow'))
        if args.deployments:
            if args.roaming:
                get_roamingComputers(args.profile)
            if args.tunnel:
                get_tunnels(args.profile)
            if args.networks:
                get_networks(args.profile)
            if args.internalNetworks:
                get_internalNetworks(args.profile)
            if args.sites:
                get_sites(args.profile)
            if args.test:
                checkPassword(args.profile)
            if args.virtualAppliances:
                get_vas(args.profile)
            if args.networkDevices:
                get_networkDevices(args.profile)
            if args.policies:
                get_policies(args.profile)
            if args.domains:
                get_internalDomains(args.profile)

        # if args.policies:
        #    print(colored('Test List Policies API', 'yellow'))
        if args.reports:
            print(colored('Test List Reports API', 'yellow'))
    elif args.update:
        if args.auth:
            print(colored('Test Update Authentication API', 'yellow'))
        if args.admin:
            print(colored('Test Update Admin API', 'yellow'))
        if args.deployments:
            print(colored('Test Update Deployments API', 'yellow'))
        if args.policies:
            print(colored('Test Update Policies API', 'yellow'))
        if args.reports:
            print(colored('Test Update Reports API', 'yellow'))
    elif args.delete:
        if args.auth:
            print(colored('Test Delete Authentication API', 'yellow'))
        if args.admin:
            print(colored('Test Delete Admin API', 'yellow'))
        if args.deployments:
            print(colored('Test Delete Deployments API', 'yellow'))
        if args.policies:
            print(colored('Test Delete Policies (Dest Lists) API', 'yellow'))
        if args.reports:
            print(colored('Test Delete Authentication API', 'yellow'))
    elif args.setup:
        setup(args)
    else:
        print(colored(
            'Argument not recognize, use "UmbrellaAPI.py -h" for more information', 'yellow'))
