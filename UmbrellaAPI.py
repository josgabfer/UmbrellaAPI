import argparse
import os
from termcolor import colored
from Modules.Core.ArgRouter import argument_router
from datetime import datetime
from dotenv import dotenv_values
import dotenv
import json


def setup(args):
    """Creates the config.json file.
    This file contains settings like the path to save the reports created by the API, or API name profiles."""

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


def main():
    parser = argparse.ArgumentParser(description='Umbrella API interface')
    setup_group = parser.add_argument_group('setup')
    setup_group.add_argument('-n', '--name', dest='name', metavar='', type=str,
                             help='Use with the Key and the Secret to create a new profile or login for the Umbrella API')
    setup_group.add_argument('-k', '--key', dest='key', metavar='', type=str,
                             help='This value is the key created from your Umbrella Dashboard')
    setup_group.add_argument('-s', '--secret', dest='secret', metavar='', type=str,
                             help='This value stores the secret created from your Umbrella Dashboard')
    setup_group.add_argument('-De', '--des', dest='des', metavar='', type=str,
                             help='This value stores the description of a given profile created.')
    setup_group.add_argument('-Pa', '--path', dest='path', metavar='', type=str,
                             help='This value instructs the program where to save the the files or reports you create')
    setup_group.add_argument('-p', '--profile', dest='profile', metavar='', type=str,
                             help='This value tells the program what profile to use, if not entered, the system will use the default profile')
    setup_group.add_argument('-Co', '--config', action='store_true',
                             help='The config argument let\'s you see the configured profiles and paths saved into the .env file')
    switch_group = parser.add_argument_group('switch')
    switch_group.add_argument('-x', '--xml', action='store_true',
                              help='The xml switch can be used to read an XML file instead of a default CSV file while creating destination lists')

    module_group = parser.add_mutually_exclusive_group(required=True)
    module_group.add_argument('-AU', '--auth', action='store_true',
                              help='Access Authentication module options, use with action arguments [-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-AD', '--admin', action='store_true',
                              help='Access Admin module options, use with action arguments[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-D', '--deployments', action='store_true',
                              help='Access Deployments module options, use with action arguments[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-Po', '--policies', action='store_true',
                              help='Access Policies module options, use with action arguments[-c --> Create, -r --> read, -u --> update, l --> list]')
    module_group.add_argument('-R', '--reports', action='store_true',
                              help='Access Report module options, use with action arguments[l --> list]')
    module_group.add_argument('-S', '--setup', action='store_true',
                              help='Access the setup module, use with action arguments (see setup options)')

    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument('-c', '--create', action='store_true',
                              help='The create action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-l', '--list', action='store_true',
                              help='The list action operator, it should be used with the Auth, Admin, Deployment, Policies or Reports module')
    action_group.add_argument('-u', '--update', action='store_true',
                              help='The update action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    action_group.add_argument('-d', '--delete', action='store_true',
                              help='The delete action operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')

    deployment_group = parser.add_mutually_exclusive_group(required=False)
    deployment_group.add_argument('-r', '--roaming', action='store_true',
                                  help='The roaming operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-t', '--tunnel', action='store_true',
                                  help='The tunnel operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-nw', '--networks', action='store_true',
                                  help='The network operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-dl', '--destination', action='store_true',
                                  help='The destination lists operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-id', '--domains', action='store_true',
                                  help='The domains operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-in', '--internalNetworks', action='store_true',
                                  help='The internal networks operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-st', '--sites', action='store_true',
                                  help='The sites operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-va', '--virtualAppliances', action='store_true',
                                  help='The virtual appliances operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument('-nd', '--networkDevices', action='store_true',
                                  help='The network devices operator, it should be used with the Auth, Admin, Deoployment, Policies or Reports module')
    deployment_group.add_argument(
        '-Te', '--test', action='store_true', help='test')
    args = parser.parse_args()

    argument_router(args)


if __name__ == '__main__':
    main()
