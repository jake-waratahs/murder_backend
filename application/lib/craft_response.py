import json
from flask import Response


def craft_response(status, message):
    data = json.dumps({"status": status, "message": message})
    return Response(data, status=status, mimetype="application/json")