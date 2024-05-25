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

By Hero:
- Hero scalability
- Hero impact
- Hero winrate (By patch)
'''

import requests
import json
import sqlite3
import pandas as pd
import numpy as np
OPEN_DOTA_URL = f'https://api.opendota.com/api/'

class DataPreprocesser():
    def __init__(self):
        self.data = pd.DataFrame()
        self.matches = pd.DataFrame()
        self.players = pd.DataFrame()

    
    def request_data(self, source):
        response = requests.get(source)  # Returns my information
        if response.status_code == 200:
            return response.json()
        
        else:
            print(f"Error: {response.status_code}")
            return None

    def player_info(self):
        pass


    def match_info(self):
        new_matches = self.request_data(OPEN_DOTA_URL + '/proMatches')
        print(len(new_matches))



    def ward_info(self):
        pass


    def split(self, data):
        pass
