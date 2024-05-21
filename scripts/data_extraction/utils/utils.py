import requests
import os
import json
import pandas as pd
from datetime import datetime

def extract_users_api():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        users_data = response.json()
        return users_data
    else:
        r = response
        message =  "HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text)
        print(message)

def format_data(res):
    data = {}
    # Flat values
    data['id']= res['id']
    data['name']= res['name']
    data['email']= res['email']
    data['phone']= res['phone']
    data['website']= res['website']
    # Nested values
    data['street']= res['address']['street']
    data['suite']= res['address']['suite']
    data['city']= res['address']['city']
    data['zipcode']= res['address']['zipcode']
    # geo data
    data['lat']= res['address']['geo']['lat']
    data['lng']= res['address']['geo']['lng']
    # company data
    data['companyname']= res['company']['name']
    data['catchPhrase']= res['company']['catchPhrase']
    data['bs']= res['company']['bs']
    return data

def export_to_json(output_directory,data,filename):
    os.makedirs(output_directory, exist_ok=True)
    file_path = os.path.join(output_directory, filename)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f'{filename} file has been exported to {file_path}')