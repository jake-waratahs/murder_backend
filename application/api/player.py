from flask import request, Response
from flask_jwt import jwt_required

from application import app, db
from application.model import Player
from application.lib.jwt import admin_required
from application.lib.craft_response import craft_response

import json

@app.route("/players", methods=["GET"])
@jwt_required()
@admin_required
def get_players():
    players = Player.query.all()
    data = json.dumps([player.serialize() for player in players])
    return Response(data, status=200, mimetype="application/json")

@app.route("/players/<int:id>", methods=["GET", "PUT"])
@jwt_required()
@admin_required
def manage_player(id):
    player = Player.query.filter_by(id=id).first_or_404()
    if request.method == "GET":
        return get_player(player)
    elif request.method == "PUT":
        return edit_player(player)


def get_player(player):
    data = json.dumps(player.serialize())
    return Response(data, status=200, mimetype="application/json")

def edit_player(player):
    admin = player.admin
    request_data = request.get_json()

    if "admin" in request_data:
        admin = request_data["admin"]

    player.admin = admin
    db.session.commit()
    return craft_response(200, "User updated successfully")