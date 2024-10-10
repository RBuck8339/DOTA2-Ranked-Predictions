import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, jsonify
from DataPreprocessing import DataPreprocesser


app = Flask(__name__)
my_processor = DataPreprocesser()
model = pickle.load(open('model.pkl', 'rb'))  # Need to generate this


# Needs testing
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
@app.route('/get_data', methods=["POST"])
def runModel():
    data = request.json
    print(data)
    data = pd.DataFrame(data)
    data, res_match = format_data(data)  # Need to modify to actually format the correct data
    res = model.predict(data)
    results = {}
    # Add code here to display scores, confidence, etc.
    return jsonify(results)


# Get random matches to populate the data table
@app.route('/predict', methods=["GET"])
def getData():
    my_processor.to_dataframes()
    matches = my_processor.matches_processed()
    random_match_num = np.random.choice(matches)
    curr_match = my_processor.players[my_processor.players['match_id'] == random_match_num]
    match = curr_match.to_json(orient='records')  # Might need to update 'records' to 'columns'
    return jsonify(match)  


if __name__ == "__main__":
    app.run(debug=True)

