import requests
import os
import json
import logging
from dotenv import load_dotenv

def extract_users_api():
    """
    Extract user data from the JSONPlaceholder API.
    """
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching user data: {e}")
        return None

def extract_weather_api2(latitude, longitude,api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        weather_info = {
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'lat': data['coord']['lat'],
            'lng': data['coord']['lon'],
            'country': data['sys'].get('country', 'N/A')
        }
        return weather_info
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data for coordinates ({latitude}, {longitude}): {e}")
        return None

def format_users_data(res):
    """
    Format user data from JSONPlaceholder API.
    """
    data = {
        'user_id': res['id'],
        'name': res['name'],
        'username': res['username'],
        'email': res['email'],
        'phone': res['phone'],
        'website': res['website'],
        'street': res['address']['street'],
        'suite': res['address']['suite'],
        'city': res['address']['city'],
        'zipcode': res['address']['zipcode'],
        'lat': res['address']['geo']['lat'],
        'lng': res['address']['geo']['lng'],
        'companyname': res['company']['name'],
        'catchPhrase': res['company']['catchPhrase'],
        'bs': res['company']['bs']
    }
    return data

def export_to_json(output_directory, data, filename):
    """
    Export data to JSON file.
    """
    try:
        os.makedirs(output_directory, exist_ok=True)
        file_path = os.path.join(output_directory, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f'{filename} file has been exported to {file_path}')
    except OSError as e:
        logging.error(f"Error exporting data to JSON file: {e}")
