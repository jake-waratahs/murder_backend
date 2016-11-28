from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

import os
import json
import datetime

# initialisation of the app
app = Flask(__name__)

# Set up SQL Alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This makes things quicker and turns off warnings
db = SQLAlchemy(app)

from .model import *
db.create_all()
db.session.commit()

# Set up JWT auth
from .lib.jwt import auth_handler, id_handler
app.config["JWT_AUTH_USERNAME_KEY"] = "zid"
app.config["JWT_AUTH_PASSWORD_KEY"] = "zpass"
app.config["JWT_AUTH_URL_RULE"] = "/login"
app.config["JWT_AUTH_HEADER_PREFIX"] = "Bearer"
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(days=3)
app.config["SECRET_KEY"] = os.environ["MURDER_JWT_SECRET"]
JWT(app, auth_handler, id_handler)

# LDAP setup
app.config["LDAP_URL"] = os.environ["MURDER_LDAP_URL"]

# Simple healthcheck endpoint to ensure we are running
@app.route("/_healthcheck", methods=["GET"])
def healthcheck():
    data = json.dumps({"status": "healthy"})
    resp = Response(data, status=200, mimetype="application/json")
    return resp


# Error handlers
@app.errorhandler(404)
def not_found(error=None):
    data = json.dumps({"status": 404,
        "message": request.path + " not found"})
    resp = Response(data, status=200, mimetype="application/json")
    return resp

@app.errorhandler(401)
def unauthorized(error=None):
    data = json.dumps({"status": 401,
        "message":"You are not permitted to perform that action"})
    resp = Response(data, status=200, mimetype="application/json")
    return resp    


# Import the rest of the API.
from .api import *