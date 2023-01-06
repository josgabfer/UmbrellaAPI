import json

def getPath(fileType):
    """This function will """
    with open ("config.json","r") as file:
        config = json.load(file)
    path = config[fileType]['PATH']
    return path
