# API endpoint for game management
import json
import dateutil.parser

from flask import request, Response
from flask_jwt import jwt_required

from application import app, db
from application.model import Game
from application.lib.jwt import admin_required


@app.route("/games", methods=["GET", "POST"])
@jwt_required()
@admin_required
def games():
    if request.method == "GET":
        return get_all_games()
    elif request.method == "POST":
        return new_game()


def get_all_games():
    games = json.dumps([game.serialize() for game in Game.query.all()])
    resp = Response(games, status=200, mimetype="application/json")
    return resp


def new_game():
    request_data = request.get_json()
    if not ("start_date" in request_data and "end_date" in request_data):
        data = json.dumps({"status": 400, 
            "message": "Please ensure a start date and an end date are provided"})
        return Response(data, status=400, mimetype="application/json")

    # Get the start and end dates and convert them to datetime objects
    try:
        start_date = dateutil.parser.parse(request_data["start_date"])
        end_date = dateutil.parser.parse(request_data["end_date"])
    except:
        data = json.dumps({"status": 400, 
            "message": "Invalid date format"})
        return Response(data, status=400, mimetype="application/json")

    # Make sure the end date is after the start date
    if start_date > end_date:
        data = json.dumps({"status": 400, 
            "message": "Please ensure start date is before end date"})

        return Response(data, status=400, mimetype="application/json")

    #Create and add the game object
    game = Game(start_date, end_date)
    db.session.add(game)
    db.session.commit()

    data = json.dumps({"status": 200, 
            "message": "New game created"})
    return Response(data, status=200, mimetype="application/json")
