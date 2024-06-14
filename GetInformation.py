# If data is not already generated, or more data is wanted, use this file
# Currently generates data for random matches selected in high tier ranked matches to use for predictions/analysis


import sqlite3
from DataPreprocessing import DataPreprocesser

# Database setup
connection = sqlite3.connect('dota2.db')
cursor = connection.cursor()


'''# While verifying everything works
cursor.execute('DROP TABLE IF EXISTS Matches')
cursor.execute('DROP TABLE IF EXISTS Players')
cursor.execute('DROP TABLE IF EXISTS PlayerStatsMatch')'''


MyProcesser = DataPreprocesser(connection, cursor)

# In order to allow for exiting the program early if needed
try:
    DataPreprocesser.match_info(MyProcesser)

except KeyboardInterrupt:
    DataPreprocesser.to_database(MyProcesser)