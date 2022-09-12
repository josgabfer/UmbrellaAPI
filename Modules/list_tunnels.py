import authentication
import requests
import pandas
import flatdict as flat

def get_tunnels ():
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

def main():
    tunnels = get_tunnels()
    tunnels.to_csv(r"C:\tunnels.csv", index = False)

main()

