from flask import Flask
from prepare_data import prepare_all_data_to_send, prepare_data_to_send, get_mean_of_all_users, get_mean_of_one_user
from flask import request
import json
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("ratings_data_user")
df = df.drop(["Unnamed: 0"], axis=1)

@app.route("/")
def hello():
    return "Movies API"


@app.route("/rating", methods=['POST', 'GET', 'DELETE'])
def post_rating():
    global df
    if request.method == "POST":
        json.dumps(request.get_json())
        df = df.append(request.get_json(),  ignore_index=True)
        print(df.head())
        df.to_csv("ratings_data_user")
        return json.dumps(request.get_json())
    if request.method == "GET":
        DATA = []
        iterrow = df.iterrows()
        for i in iterrow:
            dict_to_send = df.iloc[i[0]].to_dict()
            DATA.append(dict_to_send)

        return json.dumps(DATA)
    if request.method == "DELETE":
        df = df[0:0]
        print(df.head())
        df.to_csv("ratings_data_user")
        return "Delete"


@app.route("/ratings", methods = ['GET'])
def get_all_rating():

    return prepare_all_data_to_send()



@app.route("/ratings/<int:n>", methods = ['GET'])
def get_num_rating(n):
    return prepare_data_to_send(n)


@app.route("/avg-genre-ratings/all-users", methods = ['GET'])
def get_avg_genre_ratings():
    return ""

@app.route("/avg-genre-ratings/<int:id>", methods = ['GET'])
def get_avg_genre_one_ratings(id):
    return ""



if __name__ == "__main__":
    app.run(debug=True)
