import requests
import os
import json
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()  # Load variables from .env file
    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    return openweathermap_api_key

def extract_users_api():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: HTTP {response.status_code} - {response.reason}")


def extract_weather_api(locationlist):
    weather_list = []
    for location in locationlist:
        url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}"\
            .format(location[1], location[2],load_api_key())
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
        else:
            r = response
            message =  "HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text)
            print(message)
        data = {}
        data['id'] = location[0]
        data['lat']= res['coord']['lat']
        data['lng']= res['coord']['lon']
        data['weather']= res['weather'][0]['main']
        data['description']= res['weather'][0]['description'] 
        data['temp']= res['main']['temp']
        data['pressure']= res['main']['pressure']
        data['humidity']= res['main']['humidity']
        # data['grnd_level']= res['main']['grnd_level']
        # data['sea_level']= res['main']['sea_level']
        # data['wind_speed']= res['wind']['speed']
        # data['wind_deg']= res['wind']['deg']
        # data['wind_gust']= res['wind']['gust']
        # data['pressure']= res['main']['pressure']
        weather_list.append(data)
    return weather_list
def extract_weather_api2(latitude, longitude,api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'lat': data['coord']['lat'],
            'lng': data['coord']['lon'],
        }
        return weather_info
    else:
        print(f"Failed to fetch weather data for coordinates ({latitude}, {longitude})")
        return None
def format_users_data(res):
    data = {}
    # Flat values
    data['user_id']= res['id']
    data['name']= res['name']
    data['username']= res['username']
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
