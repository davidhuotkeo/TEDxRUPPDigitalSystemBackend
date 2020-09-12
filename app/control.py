from app import app
from flask import request, jsonify

SECRET_JWT_TOKEN = "b4632bbf6b691d062a5482984fea"

# GENERATE ID WITH UUID
from uuid import uuid4
generate_id = lambda : str(uuid4()).replace("-", "").upper()

from datetime import datetime
get_date = lambda : datetime.now()

# GENERATE TOKEN AND VERIFY THE TOKEN FUNCTION AND WRAPPER
import jwt
generate_token = lambda data: jwt.encode(data, SECRET_JWT_TOKEN).decode()

def jwt_verify(token: str):
    verified = False
    token = token.encode()
    try:
        if jwt.decode(token, SECRET_JWT_TOKEN):
            verified = True
    except:
        pass
    return verified

# import the decoration tool from functools
from functools import wraps
def jwt_required(function):
    """
    Running the jwt_required function before
    the passed function
    jwt_required used to verify the jwt is issued by our server or not
    return boolean value
    """
    @wraps(function)
    def wrapper():
        token = request.headers.get("Authentication")
        is_generate_from_server = jwt_verify(token)
        if not is_generate_from_server:
            return jsonify({"token": False}), 403
        return function()
    return wrapper

# DATABASE FUNCTIONS
from app.model import db
def add_to_database(object, multiple=False):
    if multiple:
        for obj in object:
            db.session.add(obj)
    else:
        db.session.add(object)
    db.session.commit()
def remove_from_database(object):
    db.session.delete(object)
    db.session.commit()

import pandas as pd

def unwrap_csv(stream_file):
    dataframe = pd.read_csv(stream_file)[["id", "name"]]
    data = dataframe.values
    objects = dataframe.set_index("id").to_dict()
    return data, objects

control_modules = {
    "general": {
        "id": generate_id,
        "date": get_date
    },
    "database": {
        "add": add_to_database,
        "remove": remove_from_database
    },
    "jwt": {
        "id": generate_token,
        "verify": jwt_verify,
        "required": jwt_required
    }
}