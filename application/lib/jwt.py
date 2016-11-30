from flask import Response
from flask_jwt import JWT, current_identity

from application import db
from application.model import Player
from application.lib.ldap_auth import authenticate

import json

def auth_handler(zid, zpass):
    name = authenticate(zid, zpass)

    if name is None:
        return None

    # Query the db
    player = Player.query.filter_by(zid=zid).first()


    # If the user does not exist, add it
    if player is None:

        admin = False # if no users exist, make the first admin.
        if len(Player.query.all()) == 0:
            admin = True

        player = Player(zid, name, admin)
        db.session.add(player)
        db.session.commit()

    # Return the user
    return player

def id_handler(payload):
    return Player.query.filter_by(id=payload["identity"]).first()

# Function decorator that requires a user to be an admin
def admin_required(func):
    def func_wrapper():
        if current_identity.admin:
            return func()
        else:
            data = json.dumps({"status": 401, "message": "You must be an admin to perform this action"})
            return Response(data, status=401, mimetype="application/json")

    return func_wrapper