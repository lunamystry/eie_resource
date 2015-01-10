from flask import request
from flask.ext.restful import Resource
from eieldap import users
import logging


logger = logging.getLogger(__name__)


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
        pass
        # errors = {}
        # error = "You need to provide both current password and new password"
        # try:
        #     required(args["password"])
        # except ValidationError as e:
        #     errors["password"] = error
        # try:
        #     required(args["new_password"])
        # except ValidationError as e:
        #     errors["new_password"] = error
        # return args, errors
