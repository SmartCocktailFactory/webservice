from flask import json

def jsonify(obj):
    return json.dumps(obj, indent=4, sort_keys=True)