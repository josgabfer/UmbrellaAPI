import json
import csv

def csvToJson(item_list):
    json_array = []
    with open(item_list, 'r', encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            json_array.append(row)
    json_string = json.dumps(json_array, indent=4)  
    json_data = json.loads(json_string)
    return json_data