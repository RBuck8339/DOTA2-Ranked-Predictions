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

import time # Just so that we don't go over allowed calls per minute


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
        # Default, most querys have no parameters
        if params == None:
            response = requests.get(source) 

        # If we have parameters to query with
        else:
            response = requests.get(source, params=params)

        if response.status_code == 200:
            return response.json()
        
        else:
            print(f"Error: {response.status_code}")
            return None


    # Calculate player stats
    # Thinking of adding: 
    #   Players winrate on the team they are on
    #   Role specific stats instead of general
    #   Not yet, but eventually winrate after X minutes
    #   Not yet, but eventually most played heros (one hot encoding)
    #   If player is on their main role
    #   Average advantages against lane opponent?
    def process_player_info(self, players, match):
        for player in players:
            player_stats = {} # Init/Reset dict

            if player['player_slot'] < 128:
                curr_team_radiant = 1
            else:
                curr_team_radiant = 0

            player_id = player['account_id']
            curr_lane = player['player_slot'] % 128

            # Calculate Players Win/Loss Ratio
            wl_dict = self.request_data(OPEN_DOTA_URL + 'players/' + str(player_id) + '/wl', None)

            # Get information from 25 most recent matches where they played this role
            params = {"limit": 25, "game_mode": 22, "lane_role_id": curr_lane}
            recent_matches = self.request_data(OPEN_DOTA_URL + 'players/' + str(player_id) + '/matches', params)

            recent_wl, recent_leaver, curr_team_wl = [], [], []  # Just counts, no real computations
            kdas, kills, deaths, assists = np.array(), np.array(), np.array(), np.array()  # To speed up computations

            # Find statistics from last 50 matches
            for curr_match in recent_matches:
                if curr_match['player_slot'] < 128:
                    curr_match_team = "Radiant"
                else:
                    curr_match_team = "Dire"

                # If player won this match
                if (curr_match_team == "Radiant" and curr_match['radiant_win'] == True) or (curr_match_team == "Dire" and curr_match['radiant_win'] == False):
                    recent_wl.append(1)
                else: 
                    recent_wl.append(0)

                # Match is not on this team, don't count it
                if (curr_match_team == "Radiant" and curr_team_radiant == 0) or (curr_match_team == "Dire" and curr_team_radiant == 1):
                    curr_team_wl.append(2)

                elif (curr_match_team == "Radiant" and curr_team_radiant == 1):
                    if(curr_match['radiant_win'] == 1):
                        curr_team_wl.append(1)
                    else:
                        curr_team_wl.append(0)
                
                elif (curr_match_team == "Dire" and curr_team_radiant == 0):
                    if(curr_match['radiant_win'] == 0):
                        curr_team_wl.append(1)
                    else:
                        curr_team_wl.append(0)


                # If the player hasnt died, don't divide by 0
                if curr_match['deaths'] > 0:
                    np.append(((curr_match['kills'] + curr_match['assits']) / curr_match['deaths']))
                else:
                    np.append(kdas, (curr_match['kills'] + curr_match['assists']))

                # Add player stats to array
                np.append(kills, curr_match['kills'])
                np.append(deaths, curr_match['deaths'])
                np.append(assists, curr_match['assists'])
                

            # Easily accessible stats
            player_stats['account_id'] = player_id
            player_stats['win_rate'] = wl_dict['win'] / (wl_dict['win'] + wl_dict['lose'])  # Calculate Lifetime win/loss percent
            player_stats['rank'] = player['rank_tier']  # Find player rank in current match

            # Calculate stats and add to dict
            player_stats['average_kda'] = np.mean(kdas)
            player_stats['average_kills'] = np.mean(kills)
            player_stats['average_deaths'] = np.mean(deaths)
            player_stats['average_assists'] = np.mean(assists)
            #player_stats['average_cs'] = 
            #player_stats['average_denies'] = 
            #player_stats['average_ward_score'] = 
            player_stats['recent_win_rate'] = (recent_wl.count(1) / len(recent_wl)) 
            player_stats['recent_times_left'] = (recent_leaver.count(1) / len(recent_leaver))
            player_stats['curr_team_wl_rate'] = curr_team_wl.count(1) / (curr_team_wl.count(1) + curr_team_wl.count(0))
            player_stats['curr_position'] = curr_lane
            player_stats['player_is_radiant'] = curr_team_radiant

            
            self.players = pd.concat([self.players, player_stats], ignore_index=True)
           
            

    # If a player is appearing anonymous
    def process_anon_player(self, players, anon_players, match):
        for player in anon_players:
            player_stats = {}
            player_stats['account_id'] = np.NaN  # Since we don't have an ID for this player
            player_stats['match_id'] = match['match_id']  # So we know which match this anonymous player belongs to
            player_stats['win_rate']= 0.50  # Nice middle ratio since unknown
            player_stats['curr_team_wl_rate'] = 0.50
            player_stats['rank'] = match['average_rank'] # Let's find the average rank of their team and plug that in

            self.players = pd.concat([self.players, player_stats], ignore_index=True)


    # So I can query the player account id and get the following stats
    # W/L ratio over X games (Could also do it by their role) only in ranked
    # Can calculate stuff like kills, deaths, assists, average match duration, if they left recently doing /players/id/matches (Also allows role param)
    # Group status may be important detail
    # Is the person on radiant or dire
    def process_players(self, match):
        print(match)  # TO REMOVE
        print(self.request_data(OPEN_DOTA_URL + '/matches/' + str(match['match_id']), None))

        players = []
        anon_players = []

        # For each player in the match, get their ID or note there isn't one
        for player in match['players']:
            if player.get('account_id') is not None:
                players.append(player)

            # Should append role, prob a dict
            else:
                anon_players.append(player)
                
        self.process_player_info(players, match)
        self.process_anon_player(players, anon_players, match)
            

    # Generate a set of new matches and find info about the players
    def match_info(self):
        new_matches = self.request_data(OPEN_DOTA_URL + '/publicMatches', params={"min_rank": 70}) # A list of 100 matches

        # Process each match individually
        for match in new_matches:
            curr_match = self.request_data(OPEN_DOTA_URL + '/matches/' + str(match['match_id']), None) # A list of 100 matches
            self.process_players(curr_match)


    def other_stats(self):
        pass

    
    # Merge Data into the format that I need and return it
    def merge(self):
        pass

    
    # If the database exists and has enough records
    def to_dataframes(self):
        self.players = pd.read_sql_query("SELECT * FROM Players", self.connection)
        self.matches = pd.read_sql_query("SELECT * FROM Matches", self.connection)

    
    def clean(self):
        self.players = self.players.drop_duplicates()
        self.matches = self.matches.drop_duplicates()