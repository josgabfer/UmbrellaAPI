# Disclaimer

This tool is a best effor created to take advantage of the Umbrella APIs. This is not an official Cisco solution, there is no official documentation for this tool, and we don't provide any official support/troubleshooting.
For the official Umbrella APIs documentation please go to: https://developer.cisco.com/docs/cloud-security/#!umbrella-introduction


# UmbrellaAPI

<!-- UmbrellaAPI is a Python program to consume data using the APIs of your Umbrella organization.

This program is divided into 5 different modules:

1- Admin Module: Provision and manage users, view roles, and manage customers for providers and customers for managed providers.

2- Auth Module: To create an OAuth 2.0 access token and UmbrellaAPI profiles.

3- Deployments Module: Provision, manage, and secure your networks, network entities, and policies

4- Policies Module:  Provision and manage destination lists and destinations.

5- Reports Module:  To programmatically read and audit real-time security information about your networks and systems -->

## Installation

<!-- Use git to clone the program to your machine -->

```bash
git clone https://github.com/josgabfer/UmbrellaAPI.git


<!-- Requirements -->
<!-- Use pip to install -->
certifi            2022.6.15.1
charset-normalizer 2.1.1
flatdict           4.0.1
idna               3.3
numpy              1.23.3
pandas             1.4.4
pip                22.2.2
python-dateutil    2.8.2
python-dotenv      0.21.0
pytz               2022.2.1
requests           2.28.1
setuptools         63.2.0
six                1.16.0
termcolor          2.0.1
urllib3            1.26.12
```

## Usage

```python
Windows: python UmbrellaAPI.py

Mac: python3 UmbrellaAPI.py

# The Umbrella API uses two files in order to execute its functions, the config.json and the .env file,

# config.json: This file contains information such as:
# DEFAULT_PROFILE: The profile that will be used if no other profile is executed during runtime.
# LOGFILES: Contains the PATH variable, the information in here will be the path where the log files will be saved.



# CONFILES: Contains the PATH variable, the information in here will be the path where the configuration files are located, configuration files may include informatio for internal domain creation, IPsec tunnel creation, etc.

# We do recommend creating a directory for your configuration files, and for the logfiles

# The config files should be named as follows:

# internal domains: domaininfo.csv
# IPsec tunnels: tunnelinfo.csv
# Networks: networkinfo.csv

# The necessary templates are available in the Templates folder, you can save them in your prefer directory, and change the value  of CONFILES in the config.json file

#Examples

# Use help to check the argument options
python UmbrellaAPI.py -h

# Create a new UmbrellaAPI Profile (This will create an .env file with the required credentials to create an OAuth 2.0 token. Optional protected profiles can be created.
python UmbrellaAPI.py -S -n <profile> -k <API Key> -s < API Secret>


# Listing


# The tool requires specific options to get the data
# -D seeks the Deployment API
# -l is the list action operator
# -r is the roaming computers argument
    # -p is the API profile (Optional).

# Request a list of roaming computers
python UmbrellaAPI.py -D -l -r -p <profile>

# Request a list of sites
python UmbrellaAPI.py -D -l -st -p <profile>

# Request internal domains
python UmbrellaAPI.py -D -l -id -p <profile>

# Request internal networks:
python UmbrellaAPI.py -D -l -in -p <profile>

# Request network devices:
python UmbrellaAPI.py -D -l -nd -p <profile>

# Request networks:
python UmbrellaAPI.py -D -l -nw -p <profile>

# Request all policies:
python UmbrellaAPI.py -Po -l <profile>

# Request tunnels:
python UmbrellaAPI.py -D -l -t <profile>

# Request Virtual Appliances:
python UmbrellaAPI.py -D -l -va <profile>

# Creating

# To create tunnels from a file, use the included templates in the 'Templates' directory, populate the required information, and once is ready run the command:

python UmbrellaAPI.py -D -c -t -p <profile>

# -c is the create action operator.
# -t is the tunnel argument
# -p is the API profile (Optional).


# Create Internal Domains from a file:
python UmbrellaAPI.py -D -c -id -p <profile>


# Create Internal Networks from a file:
python UmbrellaAPI.py -D -c -in -p <profile>

# When creating internal networks, make sure you have the site ID, tunnel ID, or Network ID, you can use the list -l argument to get this information.

# Create destination lists:
# When creating destination lists use the included templates in the 'Templates folder'.
# 1- First use the destlisinfo.csv to enter the name of the destination list, and the type ([1] DNS, [2] Web). When creating a DNS destination list, enter the action ('Allow' or 'Block'). When creating a Web destination list, you can just enter' Allow' as the action is irrelevant.

# 2- After you have created the destlistinfo.csv, modify the name of the destinations_name.csv by replacing the word 'name' with the destination list entered in destlistinfo.csv, if there are more than one entries in destlistinfo.csv add as many destinations_name.csv as you need.

# 3- Run the command:
python UmbrellaAPI.py -Po -c -dl -p <profile>

# WSA custom URL migration
# If you have WSA and wish to migrate your custom URLs to Umbrella SIG, export your configuration file to xml: https://www.cisco.com/c/en/us/td/docs/security/wsa/wsa_12-0/user_guide/b_WSA_UserGuide_12_0/b_WSA_UserGuide_11_7_chapter_010110.html#task_1354146

# Once you have the file exported, rename the file to destlistinfo.xml and place it in the same where all your configuration files are located, check your config.json to find this location.

# After placing the destlistinfo.xml in your configuration directory, run the command:
python3.10 UmbrellaAPI.py -Po -c -dl -x

# In this case the -x argument will tell the script to find the xml file, and create the necessary documents to push the destination lists, you will see the destlistinfo.csv modified and other files that get created with the structure of destinations_[name].csv, where 'name' changes based on the custom URL name, you can open the files to make sure they are correct. Once ready just run the command:

python3.10 UmbrellaAPI.py -Po -c -dl

# Without the -x argument, the script will now push all the custom URLs to Umbrella as we destination lists.

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
