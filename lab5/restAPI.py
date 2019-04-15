from flask import Flask
from flask import request, jsonify 
import json
import pandas as pd

from api_logic import ApiLogic
#powinien umożliwiać ZAPIS kolejnych wierszy tabeli -> POST -> /rating
#powinien umożliwiać ODCZYT  -> GET ->/ratings
#powinien umożliwiać KASOWANIE  -> DELETE ->/ratings
#powinien umożliwiać ODCZYT słownika zawierającego średnie oceny udzielone filmom poszczególnych gatunków -> GET -> /avg-genre-ratings/all-users
#powinien umożliwiać ODCZYT aktualnego profilu użytkownika -> GET ->  /avg-genre-ratings/user<userID>


app = Flask(__name__)
api = ApiLogic()

@app.route("/")
def hello():
    return "Movies API"


@app.route("/rating", methods=['POST'])
def save_rating():
    if request.method == "POST":
        result = json.dumps(request.get_json())
        print(result)
        api.add_new_rating(result)
        return result


@app.route("/ratings", methods = ['GET'])
def get_ratings():
     if request.method == "GET":
        result = api.show_all_ratings()
        print(result)
        return jsonify(result)
    # if request.method == "DELETE":
    #     #api.del_row_from_data(id)
    #     return "Deleting..."
    




@app.route("/avg-genre-ratings/all-users", methods = ['GET'])
def get_avg_genre_ratings():
    return jsonify(api.get_mean_for_all_user_all_genres())

@app.route("/avg-genre-ratings/<int:id>", methods = ['GET'])
def get_avg_genre_user_ratings(id):
    return jsonify(api.show_rating_for_user(id))


    


if __name__ == "__main__":
    app.run()
