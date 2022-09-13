import authentication
import requests
import pandas
import flatdict as flat

#User variables - can be changed
path = r"C:\tunnels2.csv"

def get_tunnels ():
    try:
        token = authentication.retrieve_token()
        url = "https://api.umbrella.com/deployments/v2/tunnels"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        response = requests.request("GET", url, headers = headers)
        if (response.status_code == 401 or response.status_code == 403):
            authentication.generate_token()
            return get_tunnels()
        elif response.status_code == 200:
            tunnels_json = response.json()
            for item in range(len(tunnels_json)):
                tunnels_json[item] = flat.FlatDict(tunnels_json[item])
            return pandas.DataFrame(tunnels_json)
    except:
        print()

def main():
    try:
        tunnels = get_tunnels()
        tunnels.to_csv(path, index = False)
    except(AttributeError):
        print("Failed to convert GET response to CSV. Check if the API Path defined in variable 'URL' is correct.")
    except(PermissionError):
        print("""Failed to save the CSV file. Check if a valid path and file name were saved in the variable 'path'.
        Make sure you don't have a CSV file open with the same name""")

main()

