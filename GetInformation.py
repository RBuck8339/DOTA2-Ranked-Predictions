import pandas as pd
import sqlite3
import requests
import json

# Database setup
connection = sqlite3.connect('dota2.db')
cursor = connection.cursor()


OPEN_DOTA_URL = f'https://api.opendota.com/api/'


#response = requests.get(OPEN_DOTA_URL + '/proPlayers')  # Returns json for every single pro player
#response = requests.get(OPEN_DOTA_URL + '/proMatches')  # Returns json for every single match
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071')  # Returns json for information about team X
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071/players')  # Returns json for every single player on team X

def get_match():
    endpoint = OPEN_DOTA_URL + '/teams/9088071/heroes'
    response = requests.get(endpoint)  # Returns my information
    if response.status_code == 200:
        return response.json()
    
    else:
        print(f"Error: {response.status_code}")
        return None


def save_match():
    pass


def api_calls():
    pass


def generate_model_data():
    myfile = get_match()
    print(myfile)

generate_model_data()