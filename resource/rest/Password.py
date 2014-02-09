from flask import request
from flask import jsonify
from flask.views import MethodView
from flask.ext.restful import Resource
from flask.ext.restful import abort
import uuid
import hashlib
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from resource.validators import required
from resource.validators import length
from resource.validators import ValidationError
from resource import app
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
        pass

    def authenticate(self, username, password):
        return users.authenticate(username, password)

    def validate(self, args):
        errors = {}
        error = "Username or Password error"
        try:
            required(args["username"])
        except ValidationError as e:
            errors["username"] = error
        try:
            required(args["password"])
        except ValidationError as e:
            errors["password"] = error
        return args, errors
