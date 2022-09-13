import requests
import base64
import os
import dotenv
from pathlib import Path

"""Environment variables - Here we load the variables KEY, SECRET, and TOKEN from the .env file to their corresponding variables. Don't change these variables from this python code.
Any changes in the variables should be done in the .env file."""
dotenv.load_dotenv()



def retrieve_token():
    """We start by checking the token variable. If token is None it means that the variable in the .env file does not exist, so we call generate_token() to create a new token and save it in the .env file as 'TOKEN'.
    If the variable 'TOKEN' exists in the .env file, we send a dummy get request using the stored token. If the response status code is 200 it means the token is valid so we return the stored token.
    If the response status code is 401 or 403 it means that the token has expired or is invalid, so we call generate_token() to create a new token and save it in the .env file."""
    """hello"""
    token = os.getenv('TOKEN')
    if (token == None):
        return generate_token()
    else:
        return token

def generate_auth_string():
    """Here we encode the API Secret and Key in base64 format needed for the generate_token() function to request an access token."""
    key = os.getenv('KEY')
    secret = os.getenv('SECRET')
    auth_string = f"{key}:{secret}"
    message_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_auth = base64_bytes.decode('ascii')
    return (base64_auth)

def generate_token():
    """Here we request the Umbrella access token using the key:secret values encoded in base64 format. 
    Token_response will store the GET response in json format. We then create an environment variable called 'TOKEN' and set said variable with the access token.
    doenv.set_key() is used to save the TOKEN variable inside the .env file."""
    dotenv_file = dotenv.find_dotenv()
    auth_string = generate_auth_string()
    url = "https://api.umbrella.com/auth/v2/token"
    headers = {
        "Authorization": "Basic " + auth_string
    }
    response = requests.request("GET", url, headers = headers)
    token_response = response.json()
    os.environ["TOKEN"] = token_response.get("access_token")
    dotenv.set_key(dotenv_file, "TOKEN", os.environ["TOKEN"])
    return token_response.get("access_token")


