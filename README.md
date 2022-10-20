# UmbrellaAPI

UmbrellaAPI is a Python program to consume data using the APIs of your Umbrella organization.

This program is divided into 5 different modules:

1- Admin Module: Provision and manage users, view roles, and manage customers for providers and customers for managed providers.

2- Auth Module: To create an OAuth 2.0 access token and UmbrellaAPI profiles.

3- Deployments Module: Provision, manage, and secure your networks, network entities, and policies

4- Policies Module:  Provision and manage destination lists and destinations.

5- Reports Module:  To programmatically read and audit real-time security information about your networks and systems

## Installation

Use git to clone the program to your machine

```bash
git clone https://github.com/josgabfer/UmbrellaAPI.git
```

## Usage

```python
Windows: python UmbrellaAPI.py

Mac: python3 UmbrellaAPI.py

#Examples

# Use help to check the argument options 
python UmbrellaAPI.py -h

# Create a new UmbrellaAPI Profile (This will create an .env file with the required credentials to create an OAuth 2.0 token. 
python UmbrellaAPI.py -S -n {Profile-Name} -k {API Key} -s {API Secret}

# Request a list of roaming computers
python UmbrellaAPI.py -D -l -r -p {Profile-Name}

# The tool requires specific options to get the data
# -D seeks the Deployment API
# -l is the list action operator
# -r is the roaming computers argument
# -p to use an API profile, you have multiple profiles.

# Create Tunnels from a file:

python UmbrellaAPI.py -D -c -t -p <profile>

# -c is the create action operator.
# -t is the tunnel argument
# -p is the API profile.

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
