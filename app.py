import pickle
import pandas as pd
import numpy as np
import sqlite3
from flask import Flask, Response, request, render_template, jsonify

from DataPreprocessing import DataPreprocesser


app = Flask(__name__)

connection = sqlite3.connect('dota2.db', check_same_thread=False)
cursor = connection.cursor()
my_processor = DataPreprocesser(connection, cursor)
model = pickle.load(open('model/model.pkl', 'rb'))  # Need to generate this


# Formats data for prediction based on what is in the JS table
def format_data(data):
    row_data = []  # List to store the row data

    # Loop through each row
    for idx, row in data.iterrows():
        row_data.extend(row.values)

    return pd.DataFrame([row_data])  # Make the data into a dataframe


@app.route('/')
def home():
    return render_template('main_page.html')


# When the button is clicked, retrieve the data from the data table and obtain a match prediction
@app.route('/predict', methods=["POST"])
def runModel():
    data = request.get_json()
    data = pd.DataFrame(data)
    print(data)  # Tmp
    data, res_match = format_data(data)  # Need to modify to actually format the correct data
    res = model.predict(data)
    results = {}
    # Add code here to display scores, confidence, etc.
    return jsonify(results)


# Get random matches to populate the data table
@app.route('/get_data', methods=["GET"])
def getData():
    my_processor.to_dataframes()
    matches = my_processor.matches_processed
    all_matches = [arr[0] for arr in matches]
    random_match_num = np.random.choice(all_matches)
    curr_match = my_processor.players[my_processor.players['match_id'] == random_match_num]
    curr_match = curr_match.drop(columns=['match_id', 'account_id'])

    # Transpose the dataframe and format it for ease of use in backend
    curr_match = curr_match.T  
    curr_match.columns = ['Radiant Position 1', 'Radiant Position 2', 'Radiant Position 3', 'Radiant Position 4', 'Radiant Position 5',
                          'Dire Position 1', 'Dire Position 2', 'Dire Position 3', 'Dire Position 4', 'Dire Position 5']
        
    match = curr_match.to_json(orient='split')  # Split is easiest to use for my purposes
    return Response(response=match, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)


