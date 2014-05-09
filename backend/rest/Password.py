from flask import request
from flask import jsonify
from flask.views import MethodView
from flask.ext.restful import Resource
from flask.ext.restful import abort
from backend.validators import required
from backend.validators import length
from backend.validators import ValidationError
from backend import app
from eieldap.models import users
from eieldap import logger


class Password(Resource):
    def get(self, username, session_key):
        return "{'result': 'NOT IMPLEMETED'}", 500

    def post(self):
        return "{'result': 'NOT IMPLEMETED'}", 500

    def delete(self):
        return "{'result': 'NOT IMPLEMETED'}", 500

    def put(self, username, session_key):
        args = request.json
        data, errors = self.validate(args)
        if errors:
            return errors, 401
        password = data["password"]
        new_password = data["new_password"]
        if self.authenticate(username, password):
            if users.change_password(username, password, new_password):
                return "Done", 201
            else:
                return "There was a server problem", 500
        else:
            return "Username and password don't match", 401

    def authenticate(self, username, password):
        return users.authenticate(username, password)

    def validate(self, args):
        errors = {}
        error = "You need to provide both current password and new password"
        try:
            required(args["password"])
        except ValidationError as e:
            errors["password"] = error
        try:
            required(args["new_password"])
        except ValidationError as e:
            errors["new_password"] = error
        return args, errors
