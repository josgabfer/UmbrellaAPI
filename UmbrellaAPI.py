import argparse
import os
from termcolor import colored
from pathlib import Path
from Modules.Auth.getToken import check_token
from Modules.Deployments.roaming_computers import RequestRoamingClients 
from Modules.Deployments.list_tunnels import  get_tunnels
from Modules.Deployments.list_networks import get_networks
from datetime import datetime
from dotenv import dotenv_values 
import dotenv


def setup(args):
    """Creates the config.json file.
    This file contains settings like the path to save the reports created by the API, or API name profiles."""

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    if args.config:
        config = dotenv_values()
        res = [val for key, val in config.items() if 'PROFILE' in key]
        print(colored('+++++++Profiles+++++++','green'))
        for val in res:
            print('Profile: ', val)
        res = [val for key, val in config.items() if 'PATH' in key]
        print(colored('+++++++Paths+++++++','green'))

        for val in res:
            print('Path: ', val)

        


    if not args.name:
        if args.path:
            dotenv.set_key(dotenv_file, 'PATH', args.path)
    else:
        key_name = args.name + '_KEY'
        secret_name = args.name + '_SECRET'
        profile_name = 'PROFILE_' + args.name

        dotenv.set_key(dotenv_file, profile_name, args.name)
        dotenv.set_key(dotenv_file, key_name, args.key)
        dotenv.set_key(dotenv_file, secret_name, args.secret)


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
    if args.create:
        if args.auth:
            print('Crear Auth')
        if args.admin:
            print('Crear Admin')
        if args.deployments:
            print('Crear Deployments')
        if args.policies:
            print('Crear Policies')
        if args.reports:
            print('Crear Reportes')
    elif args.list:
        if args.auth:
            print('Listar Auth')
        if args.admin:
            print('Listar Admin')
        if args.deployments:
            if args.roaming:
                RequestRoamingClients(args.profile)
            if args.tunnel:
                get_tunnels(args.profile)
            if args.networks:
                get_networks(args.profile)
        if args.policies:
            print('Listar Policies')
        if args.reports:
            print('Listar Reportes')
    elif args.update:
        if args.auth:
            print('Actualizar Auth')
        if args.admin:
            print('Actualizar Admin')
        if args.deployments:
            print('Actualizar Deployments')
        if args.policies:
            print('Actualizar Policies')
        if args.reports:
            print('Actualizar Reportes')
    elif args.delete:
        if args.auth:
            print('Borrar Auth')
        if args.admin:
            print('Borrar Admin')
        if args.deployments:
            print('Borrar Deployments')
        if args.policies:
            print('Borrar Policies')
        if args.reports:
            print('Borrar Reportes')
    elif args.setup:
        setup(args)
    else:
        print(f'Usage: UmbrellaAPI.py [-h] [-o] [-k] [-s] [-n] [-p] [-S | -q | -w | -ct]')





def main():
    parser = argparse.ArgumentParser(description='Umbrella API interface')
    # subparsers = parser.add_subparsers(help='sub-command help')
    setup_group = parser.add_argument_group('setup')
    setup_group.add_argument('-n','--name', dest='name', metavar='',type=str, help='Use with the Key and the Secret to create a new profile or login for the Umbrella API')
    setup_group.add_argument('-k','--key', dest='key',metavar='', type=str, help='This value is the key created from your Umbrella Dashboard')
    setup_group.add_argument('-s','--secret', dest='secret', metavar='',type=str, help='This value stores the secret created from your Umbrella Dashboard')
    setup_group.add_argument('-De','--des', dest='des', metavar='',type=str, help='This value stores the description of a given profile created.')
    setup_group.add_argument('-Pa','--path', dest='path', metavar='',type=str, help='This value instructs the program where to save the the files or reports you create')
    setup_group.add_argument('-p','--profile', dest='profile', metavar='',type=str, help='This value tells the program what profile to use, if not entered, the system will use the default profile')
    setup_group.add_argument('-Co','--config', action='store_true', help='The config argument let\'s you see the configured profiles and paths saved into the .env file')




    module_group = parser.add_mutually_exclusive_group(required=True)
    module_group.add_argument('-AU', '--auth', action='store_true', help='Access Authentication module options [-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-AD', '--admin', action='store_true', help='Access Admin module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-D', '--deployments', action='store_true', help='Access Deployments module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-P', '--policies', action='store_true', help='Access Policy module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-R', '--reports', action='store_true', help='Access Report module options[l --> list]')
    module_group.add_argument('-S', '--setup', action='store_true', help='Access the setup module to create the config file')

    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument('-c','--create', action='store_true', help='The create action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-l','--list', action='store_true', help='The list action operator, it should be used with the Auth, Admin, Deployment, Policies or Reports module')
    action_group.add_argument('-u','--update', action='store_true', help='The update action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-d','--delete', action='store_true', help='The delete action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')


    deployment_group = parser.add_mutually_exclusive_group(required=False)
    deployment_group.add_argument('-r','--roaming', action='store_true', help='The roaming deployment operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-t','--tunnel', action='store_true', help='The tunnel deployment operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-nw','--networks', action='store_true', help='The network deployment operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')    
    args = parser.parse_args()

    argument_router(args)


if __name__ =='__main__':
    main()
