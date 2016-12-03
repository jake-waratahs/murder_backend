# API endpoint for game management
import json
import dateutil.parser
from datetime import datetime

from flask import request, Response
from flask_jwt import jwt_required

from application import app, db
from application.model import Game
from application.lib.jwt import admin_required
from application.lib.craft_response import craft_response

@app.route("/games", methods=["GET", "POST"])
@jwt_required()
@admin_required
def games():
    if request.method == "GET":
        return get_all_games()
    elif request.method == "POST":
        return new_game()


@app.route("/games/<int:id>", methods=["GET", "PUT"])
@jwt_required()
@admin_required
def manage_game(id):
    if request.method == "GET":
        return get_game(id)
    elif request.method == "PUT":
        return modify_game(id)



def get_game(id):
    game = Game.query.filter_by(id=id).first_or_404()
    data = json.dumps(game.serialize())
    return Response(data, status=200, mimetype="application/json")


@app.route("/games/current", methods=["GET"])
def current_game():
    game = Game.query.filter(Game.start_date < datetime.now(), Game.end_date > datetime.now()).first_or_404()
    data = json.dumps(game.serialize())
    return Response(data, status=200, mimetype="application/json")


@app.route("/games/upcoming", methods=["GET"])
def upcoming_games():
    games = Game.query.filter(Game.start_date < datetime.now())
    data = json.dumps([game.serialize() for game in games])
    return Response(data, status=200, mimetype="application/json")


def get_all_games():
    games = json.dumps([game.serialize() for game in Game.query.all()])
    resp = Response(games, status=200, mimetype="application/json")
    return resp


def new_game():
    request_data = request.get_json()
    if not ("start_date" in request_data and "end_date" in request_data):
        return craft_response(400, "Please ensure a start date and an end date are provided")

    if "name" not in request_data:
        return craft_response(400, "Please ensure a name is provided")
    name = request_data["name"]

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
    game = Game(name, start_date, end_date)
    db.session.add(game)
    db.session.commit()
    return craft_response(200, "New game created")
    
def modify_game(id):
    request_data = request.get_json()

    game = Game.query.filter_by(id=id).first_or_404()

    start_date = game.start_date
    end_date = game.end_date
    name = game.name

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

    if "name" in request_data:
        name = request_data["name"]

    game.name = name
    game.start_date = start_date
    game.end_date = end_date
    db.session.commit()

    return craft_response(200, "Game successfully updated")