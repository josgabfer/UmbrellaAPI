import argparse
import os
from termcolor import colored
from pathlib import Path
from Modules.Auth.getToken import check_token
from Modules.Deployments.roaming_computers import RequestRoamingClients
from datetime import datetime
import json




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
                RequestRoamingClients('X')
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
    else:
        print(f'Usage: UmbrellaAPI.py [-h] [-o] [-k] [-s] [-n] [-p] [-S | -q | -w | -ct]')





def main():
    parser = argparse.ArgumentParser(description='Umbrella API interface')
    subparsers = parser.add_subparsers(help='sub-command help')

    #Auth options
    # auth_parser = subparsers.add_parser(help='Authentication Module help')
    # parser.add_argument('-k','--key', dest='key',metavar='', type=str, help='This value is the key created from your Umbrella Dashboard')
    # parser.add_argument('-s','--secret', dest='secret', metavar='',type=str, help='This value stores the secret created from your Umbrella Dashboard')
    # parser.add_argument('-n','--name', dest='name', metavar='',type=str, help='This value represents the new credentials for the connection')
    # parser.add_argument('-t','--token-type', dest='token_type', metavar='',type=str, help='This argument requires an option to set the token type, either (A: Admin, D: Deployments, P: Policies, R: Reports, X: Custom)')
    # parser.add_argument('-l','--list', action='store_true', help='The list operator, it should be used with the Aut, Admin, Deoployment, Policies or Reports module')
    # parser.add_argument('-r','--roaming', action='store_true', help='The roaming operator, access  ')

    module_group = parser.add_mutually_exclusive_group(required=True)
    module_group.add_argument('-AU', '--auth', action='store_true', help='Access Authentication module options [-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-AD', '--admin', action='store_true', help='Access Admin module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-D', '--deployments', action='store_true', help='Access Deployments module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-P', '--policies', action='store_true', help='Access Policy module options[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-R', '--reports', action='store_true', help='Access Report module options[l --> list]')

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-c','--create', action='store_true', help='The create action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-l','--list', action='store_true', help='The list action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-u','--update', action='store_true', help='The update action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-d','--delete', action='store_true', help='The delete action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')


    deployment_group = parser.add_mutually_exclusive_group(required=True)
    deployment_group.add_argument('-r','--roaming', action='store_true', help='The roaming deployment operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    args = parser.parse_args()

    argument_router(args)


if __name__ =='__main__':
    main()
