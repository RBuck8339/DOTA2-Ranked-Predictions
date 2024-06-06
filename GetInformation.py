from h11 import Data
import pandas as pd
import sqlite3
import requests
import json

from DataPreprocessing import DataPreprocesser, OPEN_DOTA_URL

# Database setup
connection = sqlite3.connect('dota2.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS Matches')
cursor.execute('DROP TABLE IF EXISTS Players')

# / matches/7551252460
'''
{'match_id': 7751252460, 'duration': 1240, 'start_time': 1716458530, 
'radiant_team_id': 9302584, 'radiant_name': 'Penguin Esport', 'dire_team_id': 9297546, 
'dire_name': 'Team Lighting', 'leagueid': 15922, 'league_name': 'HIGAMES INVITATIONAL', 
'series_id': 877789, 'series_type': 1, 'radiant_score': 36, 'dire_score': 17, 
'radiant_win': True, 'version': None}
'''


# /teams/9302584/players
'''
[{'account_id': 392277500, 'name': None, 'games_played': 103, 'wins': 49, 'is_current_team_member': None}, 
{'account_id': 204481873, 'name': None, 'games_played': 63, 'wins': 34, 'is_current_team_member': None}, 
{'account_id': 125263648, 'name': None, 'games_played': 63, 'wins': 34, 'is_current_team_member': None}, 
{'account_id': 415519834, 'name': None, 'games_played': 63, 'wins': 34, 'is_current_team_member': None}, 
{'account_id': 275871536, 'name': None, 'games_played': 61, 'wins': 27, 'is_current_team_member': None}, 
{'account_id': 331398858, 'name': None, 'games_played': 59, 'wins': 32, 'is_current_team_member': None}, 
{'account_id': 302429528, 'name': None, 'games_played': 58, 'wins': 25, 'is_current_team_member': None}, 
{'account_id': 141153841, 'name': None, 'games_played': 58, 'wins': 25, 'is_current_team_member': None}, 
{'account_id': 216007257, 'name': None, 'games_played': 58, 'wins': 25, 'is_current_team_member': None}, 
{'account_id': 417202490, 'name': None, 'games_played': 18, 'wins': 10, 'is_current_team_member': None}, 
{'account_id': 178744520, 'name': 'rex.y', 'games_played': 1, 'wins': 0, 'is_current_team_member': False}]
'''


# '/publicMatches', params = {"min_rank": 70}
'''
{'match_id': 7756630500, 'match_seq_num': 6531334592, 'radiant_win': False, 'start_time': 1716651617, 'duration': 2585, 
'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 71, 'num_rank_tier': 8, 'cluster': 223, 'radiant_team': [19, 56, 97, 22, 26], 'dire_team': [28, 42, 87, 98, 88]}
'''

#response = requests.get(OPEN_DOTA_URL + '/proPlayers')  # Returns json for every single pro player
#response = requests.get(OPEN_DOTA_URL + '/proMatches')  # Returns json for every single match
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071')  # Returns json for information about team X
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071/players')  # Returns json for every single player on team X

def get_match():
    endpoint = OPEN_DOTA_URL + '/players/92580861/recentMatches'
    response = requests.get(endpoint)  # Returns my information
    if response.status_code == 200:
        return response.json()
    
    else:
        print(f"Error: {response.status_code}")
        return None

def generate_model_data():
    myfile = get_match()
    print(len(myfile))

MyProcesser = DataPreprocesser(connection, cursor)

DataPreprocesser.match_info(MyProcesser)

''' /proMatches
{'match_id': 7761976803, 'duration': 1985, 'start_time': 1716846191, 'radiant_team_id': 8849850, 'radiant_name': 'HELLBEAR HEROES', 'dire_team_id': 8849833, 
'dire_name': 'VERTEX PACK', 'leagueid': 16635, 
'league_name': 'Dota 2 Space League', 'series_id': 879062, 'series_type': 1, 'radiant_score': 24, 'dire_score': 37, 'radiant_win': False, 'version': 21}
'''


#generate_model_data()