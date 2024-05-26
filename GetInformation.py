import pandas as pd
import sqlite3
import requests
import json

from DataPreprocessing import DataPreprocesser

# Database setup
connection = sqlite3.connect('dota2.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS MATCHES")

# Thinking of using this as my target variables, with more able to be added
match_table_constructor = """CREATE TABLE MATCHES (
                    MatchID INT, 
                    radiant_team_id INT,
                    dire_team_id INT,
                    radiant_score INT,
                    dire_score INT,
                    radiant_win INT
                    )"""

teams_table_constructor = """CREATE TABLE TEAMS (
                    team_id INT,
                    player1_ INT,
                    is_radiant INT
                    )"""

# / matches/7551252460
'''
{'match_id': 7751252460, 'duration': 1240, 'start_time': 1716458530, 
'radiant_team_id': 9302584, 'radiant_name': 'Penguin Esport', 'dire_team_id': 9297546, 
'dire_name': 'Team Lighting', 'leagueid': 15922, 'league_name': 'HIGAMES INVITATIONAL', 
'series_id': 877789, 'series_type': 1, 'radiant_score': 36, 'dire_score': 17, 
'radiant_win': True, 'version': None}
'''

# /teams/9302584
'''
{'team_id': 9302584, 'rating': 1039.51, 'wins': 59, 'losses': 62, 
'last_match_time': 1716548842, 'name': 'Penguin Esport', 'tag': '', 
'logo_url': 'https://steamusercontent-a.akamaihd.net/ugc/2500138005841258778/8EBBD4EF78060F42477E53FF15DF0A131C29718C/'}
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

# /matches/7551252460
'''
{'players': [{'player_slot': 0, 'team_number': 0, 'team_slot': 0, 'hero_id': 1, 'item_0': 208, 'item_1': 250, 'item_2': 156, 'item_3': 139, 'item_4': 147, 'item_5': 137, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 362, 'kills': 10, 'deaths': 4, 'assists': 8, 'leaver_status': 0, 'last_hits': 250, 'denies': 4, 'gold_per_min': 1577, 'xp_per_min': 2416, 'level': 30, 'net_worth': 45947, 'aghanims_scepter': 1, 'aghanims_shard': 1, 'moonshard': 1, 'hero_damage': 33439, 'tower_damage': 11519, 'hero_healing': 0, 'gold': 1872, 'gold_spent': 46860, 'ability_upgrades_arr': [5003, 5004, 5003, 7314, 5004, 5006, 5004, 5004, 7314, 6250, 7314, 5006, 7314, 5003, 6012, 5003, 5006, 6606, 6353, 966, 666, 665, 6607], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': True, 'win': 1, 'lose': 0, 'total_gold': 47099, 'total_xp': 72157, 'kills_per_min': 0.33482142857142855, 'kda': 3.6, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1577, 'pct': 1}, 'xp_per_min': {'raw': 2416, 'pct': 1}, 'kills_per_min': {'raw': 0.3348214285714286, 'pct': 0.8391364902506964}, 'last_hits_per_min': {'raw': 8.370535714285715, 'pct': 0.5188022284122563}, 'hero_damage_per_min': {'raw': 1119.609375, 'pct': 0.9428969359331476}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.9700557103064067}, 'tower_damage': {'raw': 11519, 'pct': 0.7332869080779945}}}, 
{'player_slot': 1, 'team_number': 0, 'team_slot': 1, 'hero_id': 53, 'item_0': 50, 'item_1': 250, 'item_2': 135, 'item_3': 123, 'item_4': 249, 'item_5': 158, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 288, 'kills': 10, 'deaths': 6, 'assists': 14, 'leaver_status': 0, 'last_hits': 146, 'denies': 4, 'gold_per_min': 1408, 'xp_per_min': 2160, 'level': 30, 'net_worth': 41531, 'aghanims_scepter': 1, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 28099, 'tower_damage': 11366, 'hero_healing': 0, 'gold': 5256, 'gold_spent': 38330, 'ability_upgrades_arr': [5245, 5246, 5245, 5245, 5246, 5248, 5245, 5246, 5246, 470, 5247, 5248, 5247, 5247, 5247, 6500, 5248, 927, 6539, 926, 1118, 6702], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': True, 'win': 1, 'lose': 0, 'total_gold': 42052, 'total_xp': 64512, 'kills_per_min': 0.33482142857142855, 'kda': 3.43, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1408, 'pct': 1}, 'xp_per_min': {'raw': 2160, 'pct': 1}, 'kills_per_min': {'raw': 0.3348214285714286, 'pct': 0.917312661498708}, 'last_hits_per_min': {'raw': 4.888392857142858, 'pct': 0.5663221360895779}, 'hero_damage_per_min': {'raw': 940.8147321428572, 'pct': 0.9272179155900087}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.3044788975021533}, 'tower_damage': {'raw': 11366, 'pct': 0.9194659776055125}}}, 
{'player_slot': 2, 'team_number': 0, 'team_slot': 2, 'hero_id': 87, 'item_0': 100, 'item_1': 176, 'item_2': 226, 'item_3': 273, 'item_4': 220, 'item_5': 1107, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 336, 'kills': 7, 'deaths': 12, 'assists': 26, 'leaver_status': 0, 'last_hits': 5, 'denies': 0, 'gold_per_min': 902, 'xp_per_min': 1534, 'level': 27, 'net_worth': 25868, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 26779, 'tower_damage': 144, 'hero_healing': 0, 'gold': 1618, 'gold_spent': 25950, 'ability_upgrades_arr': [5458, 5459, 5458, 5459, 5458, 5461, 5458, 5459, 5459, 1142, 5461, 5460, 5460, 5460, 5460, 788, 5461, 6215, 737, 6368], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': True, 'win': 1, 'lose': 0, 'total_gold': 26939, 'total_xp': 45815, 'kills_per_min': 0.234375, 'kda': 2.54, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 902, 'pct': 1}, 'xp_per_min': {'raw': 1534, 'pct': 1}, 'kills_per_min': {'raw': 0.234375, 'pct': 0.9629468177855275}, 'last_hits_per_min': {'raw': 0.1674107142857143, 'pct': 0.006538796861377506}, 'hero_damage_per_min': {'raw': 896.6183035714286, 'pct': 0.9969485614646905}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.6848299912816042}, 'tower_damage': {'raw': 144, 'pct': 0.43112467306015695}}}, 
{'player_slot': 3, 'team_number': 0, 'team_slot': 3, 'hero_id': 96, 'item_0': 119, 'item_1': 220, 'item_2': 600, 'item_3': 127, 'item_4': 114, 'item_5': 692, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 364, 'kills': 8, 'deaths': 5, 'assists': 29, 'leaver_status': 0, 'last_hits': 111, 'denies': 5, 'gold_per_min': 1439, 'xp_per_min': 2413, 'level': 30, 'net_worth': 41966, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 53983, 'tower_damage': 4903, 'hero_healing': 0, 'gold': 13541, 'gold_spent': 31475, 'ability_upgrades_arr': [5514, 5515, 5515, 5516, 5515, 5517, 5515, 5514, 5514, 5514, 5516, 5517, 5516, 5516, 6145, 5918, 5517, 6616, 6322, 5910, 6617, 453, 5988], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': True, 'win': 1, 'lose': 0, 'total_gold': 42978, 'total_xp': 72068, 'kills_per_min': 0.26785714285714285, 'kda': 6.17, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1439, 'pct': 1}, 'xp_per_min': {'raw': 2413, 'pct': 1}, 'kills_per_min': {'raw': 0.26785714285714285, 'pct': 0.8082253017434063}, 'last_hits_per_min': {'raw': 3.716517857142857, 'pct': 0.20295037997317836}, 'hero_damage_per_min': {'raw': 1807.466517857143, 'pct': 0.9982118909253465}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.9499329459097005}, 'tower_damage': {'raw': 4903, 'pct': 0.8042020563254358}}}, 
{'player_slot': 4, 'team_number': 0, 'team_slot': 4, 'hero_id': 26, 'item_0': 1, 'item_1': 176, 'item_2': 100, 'item_3': 123, 'item_4': 133, 'item_5': 235, 'backpack_0': 58, 'backpack_1': 214, 'backpack_2': 0, 'item_neutral': 571, 'kills': 13, 'deaths': 7, 'assists': 10, 'leaver_status': 0, 'last_hits': 54, 'denies': 2, 'gold_per_min': 1142, 'xp_per_min': 1819, 'level': 28, 'net_worth': 39890, 'aghanims_scepter': 1, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 23956, 'tower_damage': 2494, 'hero_healing': 0, 'gold': 2115, 'gold_spent': 32615, 'ability_upgrades_arr': [5044, 5046, 5044, 5046, 5044, 5047, 5044, 5045, 5046, 5046, 6600, 5047, 5045, 5045, 781, 5045, 5047, 541, 6678, 465, 401], 'personaname': 'Снежок', 'name': None, 'last_login': '2021-12-04T16:01:25.520Z', 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': True, 'win': 1, 'lose': 0, 'total_gold': 34107, 'total_xp': 54327, 'kills_per_min': 0.43526785714285715, 'kda': 2.88, 'abandons': 0, 'rank_tier': 21, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1142, 'pct': 1}, 'xp_per_min': {'raw': 1819, 'pct': 1}, 'kills_per_min': {'raw': 0.43526785714285715, 'pct': 0.9743882917905328}, 'last_hits_per_min': {'raw': 1.8080357142857144, 'pct': 0.7479990852961353}, 'hero_damage_per_min': {'raw': 802.0982142857142, 'pct': 0.9510633432426252}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.7470843814315116}, 'tower_damage': {'raw': 2494, 'pct': 0.9437457123256345}}}, 
{'player_slot': 128, 'team_number': 1, 'team_slot': 0, 'hero_id': 31, 'item_0': 108, 'item_1': 254, 'item_2': 256, 'item_3': 69, 'item_4': 90, 'item_5': 180, 'backpack_0': 218, 'backpack_1': 9, 'backpack_2': 59, 'item_neutral': 300, 'kills': 1, 'deaths': 14, 'assists': 14, 'leaver_status': 0, 'last_hits': 49, 'denies': 0, 'gold_per_min': 671, 'xp_per_min': 1354, 'level': 26, 'net_worth': 19808, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 17792, 'tower_damage': 0, 'hero_healing': 0, 'gold': 183, 'gold_spent': 20565, 'ability_upgrades_arr': [5134, 5136, 7325, 5134, 5134, 5137, 5136, 5136, 5136, 530, 5134, 5137, 7325, 7325, 6292, 7325, 5137, 531, 318], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': False, 'win': 0, 'lose': 1, 'total_gold': 20040, 'total_xp': 40439, 'kills_per_min': 0.033482142857142856, 'kda': 1, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 671, 'pct': 0.999}, 'xp_per_min': {'raw': 1354, 'pct': 1}, 'kills_per_min': {'raw': 0.033482142857142856, 'pct': 0.0665}, 'last_hits_per_min': {'raw': 1.640625, 'pct': 0.5315}, 'hero_damage_per_min': {'raw': 595.7142857142858, 'pct': 0.602}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.625}, 'tower_damage': {'raw': 0, 'pct': 0.2085}}}, 
{'player_slot': 129, 'team_number': 1, 'team_slot': 1, 'hero_id': 44, 'item_0': 208, 'item_1': 116, 'item_2': 156, 'item_3': 108, 'item_4': 1808, 'item_5': 63, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 825, 'kills': 11, 'deaths': 12, 'assists': 11, 'leaver_status': 0, 'last_hits': 87, 'denies': 5, 'gold_per_min': 1053, 'xp_per_min': 1933, 'level': 29, 'net_worth': 31619, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 35345, 'tower_damage': 0, 'hero_healing': 0, 'gold': 4069, 'gold_spent': 28295, 'ability_upgrades_arr': [5190, 5191, 5190, 5192, 5190, 5193, 5190, 5191, 5191, 483, 5191, 5193, 5192, 5192, 490, 5192, 5193, 1074, 6847, 559, 6848, 491], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': False, 'win': 0, 'lose': 1, 'total_gold': 31449, 'total_xp': 57732, 'kills_per_min': 0.3683035714285714, 'kda': 1.69, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1053, 'pct': 0.9996863237139272}, 'xp_per_min': {'raw': 1933, 'pct': 1}, 'kills_per_min': {'raw': 0.3683035714285714, 'pct': 0.7697616060225847}, 'last_hits_per_min': {'raw': 2.912946428571429, 'pct': 0.06555834378920954}, 'hero_damage_per_min': {'raw': 1183.4263392857144, 'pct': 0.9024466750313677}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.9683186951066499}, 'tower_damage': {'raw': 0, 'pct': 0.23682559598494354}}}, 
{'player_slot': 130, 'team_number': 1, 'team_slot': 2, 'hero_id': 68, 'item_0': 214, 'item_1': 166, 'item_2': 108, 'item_3': 236, 'item_4': 247, 'item_5': 40, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 675, 'kills': 2, 'deaths': 13, 'assists': 17, 'leaver_status': 0, 'last_hits': 43, 'denies': 2, 'gold_per_min': 755, 'xp_per_min': 1302, 'level': 26, 'net_worth': 18581, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 20383, 'tower_damage': 382, 'hero_healing': 0, 'gold': 3026, 'gold_spent': 16700, 'ability_upgrades_arr': [5347, 5346, 5347, 5346, 5347, 5348, 5347, 5346, 5345, 5345, 7652, 5348, 5345, 5346, 6214, 5345, 5348, 6291, 7106], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': False, 'win': 0, 'lose': 1, 'total_gold': 22549, 'total_xp': 38886, 'kills_per_min': 0.06696428571428571, 'kda': 1.36, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 755, 'pct': 0.99950884086444}, 'xp_per_min': {'raw': 1302, 'pct': 1}, 'kills_per_min': {'raw': 0.06696428571428571, 'pct': 0.18713163064833005}, 'last_hits_per_min': {'raw': 1.439732142857143, 'pct': 0.48772102161100195}, 'hero_damage_per_min': {'raw': 682.4665178571428, 'pct': 0.8894891944990176}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.6792730844793713}, 'tower_damage': {'raw': 382, 'pct': 0.5147347740667977}}}, 
{'player_slot': 131, 'team_number': 1, 'team_slot': 3, 'hero_id': 71, 'item_0': 610, 'item_1': 0, 'item_2': 249, 'item_3': 114, 'item_4': 48, 'item_5': 154, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 2192, 'kills': 11, 'deaths': 5, 'assists': 11, 'leaver_status': 0, 'last_hits': 140, 'denies': 8, 'gold_per_min': 1233, 'xp_per_min': 2438, 'level': 30, 'net_worth': 36333, 'aghanims_scepter': 1, 'aghanims_shard': 1, 'moonshard': 0, 'hero_damage': 29019, 'tower_damage': 79, 'hero_healing': 0, 'gold': 5058, 'gold_spent': 32940, 'ability_upgrades_arr': [5355, 5353, 5355, 7301, 5353, 5356, 5355, 5355, 5353, 5931, 7301, 5356, 7301, 5353, 6253, 7301, 5356, 6149, 830, 7022, 6296, 8254, 6543], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': False, 'win': 0, 'lose': 1, 'total_gold': 36825, 'total_xp': 72814, 'kills_per_min': 0.3683035714285714, 'kda': 3.67, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1233, 'pct': 1}, 'xp_per_min': {'raw': 2438, 'pct': 1}, 'kills_per_min': {'raw': 0.3683035714285714, 'pct': 0.9210263245584805}, 'last_hits_per_min': {'raw': 4.6875, 'pct': 0.8373875374875042}, 'hero_damage_per_min': {'raw': 971.6183035714286, 'pct': 0.9563478840386538}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.7617460846384538}, 'tower_damage': {'raw': 79, 'pct': 0.2622459180273242}}}, 
{'player_slot': 132, 'team_number': 1, 'team_slot': 4, 'hero_id': 11, 'item_0': 141, 'item_1': 220, 'item_2': 603, 'item_3': 249, 'item_4': 0, 'item_5': 116, 'backpack_0': 0, 'backpack_1': 0, 'backpack_2': 0, 'item_neutral': 309, 'kills': 7, 'deaths': 4, 'assists': 6, 'leaver_status': 0, 'last_hits': 243, 'denies': 7, 'gold_per_min': 1328, 'xp_per_min': 2603, 'level': 30, 'net_worth': 33624, 'aghanims_scepter': 0, 'aghanims_shard': 1, 'moonshard': 1, 'hero_damage': 30476, 'tower_damage': 3824, 'hero_healing': 0, 'gold': 2324, 'gold_spent': 38705, 'ability_upgrades_arr': [5059, 5062, 5059, 5062, 5059, 5062, 5059, 5062, 5064, 6016, 5064, 5063, 5063, 5063, 6070, 5063, 5064, 6670, 1072, 999, 6875, 815, 929], 'radiant_win': True, 'start_time': 1706024135, 'duration': 1792, 'cluster': 183, 'lobby_type': 0, 'game_mode': 23, 'is_contributor': False, 'patch': 54, 'region': 8, 'isRadiant': False, 'win': 0, 'lose': 1, 'total_gold': 39662, 'total_xp': 77742, 'kills_per_min': 0.234375, 'kda': 2.6, 'abandons': 0, 'rank_tier': None, 'is_subscriber': False, 'benchmarks': {'gold_per_min': {'raw': 1328, 'pct': 0.999746963562753}, 'xp_per_min': {'raw': 2603, 'pct': 1}, 'kills_per_min': {'raw': 0.234375, 'pct': 0.49468623481781376}, 'last_hits_per_min': {'raw': 8.136160714285715, 'pct': 0.7894736842105263}, 'hero_damage_per_min': {'raw': 1020.4017857142857, 'pct': 0.8393218623481782}, 'hero_healing_per_min': {'raw': 0, 'pct': 0.8947368421052632}, 'tower_damage': {'raw': 3824, 'pct': 0.5334008097165992}}}], 
'radiant_win': True, 'duration': 1792, 'pre_game_duration': 60, 'start_time': 1706024135, 'match_id': 7551252460, 'match_seq_num': 6358105611, 'tower_status_radiant': 1974, 'tower_status_dire': 0, 'barracks_status_radiant': 63, 'barracks_status_dire': 0, 'cluster': 183, 'first_blood_time': 121, 'lobby_type': 0, 'human_players': 10, 'leagueid': 0, 'game_mode': 23, 'flags': 0, 'engine': 1, 'radiant_score': 48, 'dire_score': 34, 'picks_bans': [{'is_pick': True, 'hero_id': 1, 'team': 0, 'order': 0}, {'is_pick': True, 'hero_id': 11, 'team': 1, 'order': 1}, {'is_pick': True, 'hero_id': 44, 'team': 1, 'order': 2}, {'is_pick': True, 'hero_id': 53, 'team': 0, 'order': 3}, {'is_pick': True, 'hero_id': 71, 'team': 1, 'order': 4}, {'is_pick': True, 'hero_id': 68, 'team': 1, 'order': 5}, {'is_pick': True, 'hero_id': 26, 'team': 0, 'order': 6}, {'is_pick': True, 'hero_id': 31, 'team': 1, 'order': 7}, {'is_pick': True, 'hero_id': 87, 'team': 0, 'order': 8}], 'od_data': {'has_api': True, 'has_gcdata': False, 'has_parsed': False}, 'metadata': None, 'patch': 54, 'region': 8}'''


# '/publicMatches', params = {"min_rank": 70}
'''
{'match_id': 7756630500, 'match_seq_num': 6531334592, 'radiant_win': False, 'start_time': 1716651617, 'duration': 2585, 
'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 71, 'num_rank_tier': 8, 'cluster': 223, 'radiant_team': [19, 56, 97, 22, 26], 'dire_team': [28, 42, 87, 98, 88]}
'''
# Can plug match id into /matches/id

cursor.execute(match_table_constructor)


OPEN_DOTA_URL = f'https://api.opendota.com/api/'


#response = requests.get(OPEN_DOTA_URL + '/proPlayers')  # Returns json for every single pro player
#response = requests.get(OPEN_DOTA_URL + '/proMatches')  # Returns json for every single match
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071')  # Returns json for information about team X
#response = requests.get(OPEN_DOTA_URL + '/teams/9088071/players')  # Returns json for every single player on team X

def get_match():
    endpoint = OPEN_DOTA_URL + '/matches/7756630500'
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

MyProcesser = DataPreprocesser(connection, cursor)

DataPreprocesser.match_info(MyProcesser)

#generate_model_data()