# Likely important stats (pregame)
'''
By Player:
- Average Kills
- Average Deaths
- Average Assists
- Average Denies
- Average Creep Score
- Average Wards
- Total Moneys
- Total gold spent
- Average Gold Per Minute
- Average Tower Damage
- Win/Loss Ratio 
- Stuns
- Damage
- Healing

For team:
- Team Composition
- First Blood Rate
- Average Roshan Kills
- Average tower kills
- Average Barracks kills
- Average Match Duration
- Early/Late game win rates
- Expected Heros

By Hero:
- Hero scalability
- Hero impact
- Hero winrate (By patch)
'''

# Two problems
'''
One: Predict match outcome only knowing pre match info (no heros) Binary Classification
Two: Predict how the match will play out knowing players and the draft Regression
'''


import requests
import json
import sqlite3
import pandas as pd
import numpy as np


OPEN_DOTA_URL = f'https://api.opendota.com/api/'

class DataPreprocesser():
    def __init__(self, connection, cursor):
        # For the SQL database
        self.connection = connection
        self.cursor = cursor

        # For data for the model
        self.data = pd.DataFrame()
        self.matches = pd.DataFrame()
        self.players = pd.DataFrame()

    
    def request_data(self, source, params):
        if params == None:
            response = requests.get(source)  # Returns my information

        # If we have parameters to query with
        else:
            response = requests.get(source, params=params)

        if response.status_code == 200:
            return response.json()
        
        else:
            print(f"Error: {response.status_code}")
            return None


    # So I can query the player account id and get the following stats
    # W/L ratio over X games (Could also do it by their role) only in ranked
    # Can calculate stuff like kills, deaths, assists, average match duration, if they left recently doing /players/id/matches (Also allows role param)
    # Group status may be important detail
    def process_player_info(self, match):
        print(match['players'])
        for player in match['players']:
            print(player)
            player_id = player['account_id']
            print(player_id)
            print("Win/Loss")
            print(self.request_data(OPEN_DOTA_URL + 'players/' + str(player_id) + '/wl', None))
            print("Recent Matches")
            params = {"limit": 5}
            print(self.request_data(OPEN_DOTA_URL + 'players/' + str(player_id) + '/matches', params))


    def match_info(self):
        new_matches = self.request_data(OPEN_DOTA_URL + '/publicMatches', params={"min_rank": 70}) # A list of 100 matches
    
        #print(new_matches)

        for match in new_matches:
            #print(match.keys())
            curr_match = self.request_data(OPEN_DOTA_URL + '/matches/' + str(match['match_id']), None) # A list of 100 matches
            self.process_player_info(curr_match)



    def ward_info(self):
        pass


    def split(self, data):
        pass

    
    def to_dataframes(self):
        self.players = pd.read_sql_query("SELECT * FROM Players", self.connection)
        self.matches = pd.read_sql_query("SELECT * FROM Matches", self.connection)

    
    def clean(self):
        self.players.drop_duplicates()
        self.matches.drop_duplicates()
