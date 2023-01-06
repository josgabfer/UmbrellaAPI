import datetime 
import json

def getPath(fileType):
    """This function will """
    with open ("config.json","r") as file:
        config = json.load(file)
    date = datetime.datetime.now()
    timestamp = date.strftime('_%Y_%m_%d_%H_%M')
    path = config[fileType]['PATH'] + 'LIST_DOMAINS_' + str(timestamp) + ".csv"
    return path
