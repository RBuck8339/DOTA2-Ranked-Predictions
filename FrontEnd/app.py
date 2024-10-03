import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, jsonify
from DataPreprocessing import DataPreprocesser


app = Flask(__name__)
my_processor = DataPreprocesser()
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=["POST"])
def runModel():
    data = request.json  # I should be able to get the data directly from the table since it should be correct
    data = pd.DataFrame(data)

    # data = ...

    # Add a way to get the latest testing scores from the model to show the users

    y_pred = model(data)

    # Return a dataframe of scores
    tmp = {}
    return jsonify(tmp)


# Get random matches to populate the data table
@app.route('/', methods=["GET"])
def getData():
    my_processor.to_dataframes()
    data = my_processor.merge_data()  # Put data into correct format for model

    # Choose a random match number
    matches = my_processor.matches_processed()
    random_match_num = np.random.choice(matches)
    curr_match = data[data == random_match_num]

    # Get the match as a json and send to back end
    match = curr_match.to_json(orient='records')
    return jsonify(match)


# Return the latest model test scores
def scores():
    pass

if __name__ == "__main__":
    app.run(debug=True)
