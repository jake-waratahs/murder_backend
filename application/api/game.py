# API endpoint for game management
import json
import dateutil.parser

from flask import request, Response
from flask_jwt import jwt_required

from application import app, db
from application.model import Game
from application.lib.jwt import admin_required
from application.lib.craft_response import craft_response

@app.route("/games", methods=["GET", "POST", "PUT"])
@jwt_required()
@admin_required
def games():
    if request.method == "GET":
        return get_all_games()
    elif request.method == "POST":
        return new_game()
    elif request.method == "PUT":
        return modify_game()


def get_all_games():
    games = json.dumps([game.serialize() for game in Game.query.all()])
    resp = Response(games, status=200, mimetype="application/json")
    return resp


def new_game():
    request_data = request.get_json()
    if not ("start_date" in request_data and "end_date" in request_data):
        return craft_response(400, "Please ensure a start date and an end date are provided")

    # Get the start and end dates and convert them to datetime objects
    try:
        start_date = dateutil.parser.parse(request_data["start_date"])
        end_date = dateutil.parser.parse(request_data["end_date"])
    except:
        return craft_response(400, "Invalid date format")

    # Make sure the end date is after the start date
    if start_date > end_date:
        return craft_response(400, "Please ensure start date is before end date")

    #Create and add the game object
    game = Game(start_date, end_date)
    db.session.add(game)
    db.session.commit()
    return craft_response(200, "New game created")
    
def modify_game():
    request_data = request.get_json()

    if "id" not in request_data:
        return craft_response(400, "ID not provided")

    game = Game.query.filter_by(id=request_data["id"]).first()

    if game is None:
        return craft_response(400, "Game does not exist")

    start_date = game.start_date
    end_date = game.end_date

    try:
        if "start_date" in request_data:
            start_date = dateutil.parser.parse(request_data["start_date"])

        if "end_date" in request_data:
            end_date = dateutil.parser.parse(request_data["end_date"])
    except:
        return craft_response(400, "Invalid date format")
    
    # TODO: Fix this.
    # if start_date > end_date:
        # return craft_response(400, "Please ensure start date is before end date")

    game.start_date = start_date
    game.end_date = end_date
    db.session.commit()

    return craft_response(200, "Game successfully updated")