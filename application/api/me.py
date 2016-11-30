# API endpoint for getting data about yoself
from application import app

from flask import Response
from flask_jwt import jwt_required, current_identity

import json

@app.route("/me")
@jwt_required()
def me():
    data = json.dumps(current_identity.serialize())
    return Response(data, status=200, mimetype="application/json")