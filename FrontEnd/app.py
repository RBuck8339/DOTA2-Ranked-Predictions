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
    data = request.json
    print(data)
    data = pd.DataFrame(data)
    my_processor.merge_data()


# Get random matches to populate the data table
@app.route('/', methods=["GET"])
def getData():
    my_processor.to_dataframes()
    matches = my_processor.matches_processed()
    random_match_num = np.random.choice(matches)
    curr_match = my_processor.players[my_processor.players['match_id'] == random_match_num]
    match = curr_match.to_json(orient='records')
    return jsonify(match)


if __name__ == "__main__":
    app.run(debug=True)

