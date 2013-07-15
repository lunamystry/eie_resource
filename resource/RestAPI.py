from flask import request
from flask import jsonify
from flask.views import MethodView
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import abort
import functools
import uuid
import hashlib
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from resource.validators import required
from resource.validators import length
from resource.validators import ValidationError
from eieldap import models
from eieldap import logger

client = MongoClient()


class Session(Resource):
    def get(self, session_id):
        session = client.resource.sessions.find_one({
            '_id': ObjectId(session_id)})
        if self.is_active(session):
            session["_id"] = str(session["_id"])
            return session
        else:
            return "{'session': 'Session not found'}", 404

    def delete(self, session_id):
        client.resource.sessions.remove({'_id': ObjectId(session_id)})
        return "", 204

    def put(self, session_id):
        session = client.resource.sessions.find_one({
            '_id': ObjectId(session_id)})
        args = request.json
        for key in args.keys():
            session[key] = args[key]
        client.resource.sessions.save(session)
        session["_id"] = str(session["_id"])
        return session, 201

    def is_active(self, session):
        now = datetime.now()
        current_tm = datetime.strptime(
            session["timestamp"], "%Y-%m-%d %H:%M:%S")
        td = now - current_tm
        if td.total_seconds() > 3600:
            return False
        return True


class Sessions(Resource):
    def get(self):
        """ Get session by like ObjectId or something, if error
        person is not logged in"""
        sessions = client.resource.sessions
        session_list = [session for session in sessions.find()]
        for session in session_list:
            session["_id"] = str(session["_id"])
            session["timestamp"] = str(session["timestamp"])
            if not Session().is_active(session):
                sessions.remove(session)
        return jsonify({"result": session_list})

    def post(self):
        """ Login means POSTing to this, this checks the credentials
        If they are valid, it returns a temporary uuid (not very secure)
        which is the session key stored in mongo"""
        args = request.json
        data, errors = self.validate(args)
        if errors:
            return errors, 500
        user = client.resource.users.find_one({'username': data["username"]})
        if(self.authenticate(data["username"], data["password"])):
            session = client.resource.sessions.find_one({
                "user_id": str(user["_id"])})
            if not session:
                session = {"user_id": str(user["_id"])}
            session["key"] = str(uuid.uuid4())
            session["timestamp"] = str(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            client.resource.sessions.save(session)
            return "session created: " + str(session["_id"]), 201
        return {"username": "Username or Password error"}, 500

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

    def authenticate(self, username, password):
        user = client.resource.users.find_one({'username': username})
        if user:
            return user["password"] == self.hashed(password, user["salt"])
        return False

    def hashed(self, password, salt):
        return hashlib.sha512(password + salt).hexdigest()


class User(Resource):
    def get(self, user_id):
        user = models.User().find_one({"uid": user_id})
        return user

    def delete(self, user_id):
        client.resource.users.remove({'_id': ObjectId(user_id)})
        return "", 204

    def put(self, user_id):
        user = client.resource.users.find_one({'_id': ObjectId(user_id)})
        args = request.values.to_dict()
        data, errors = self.validate(args)
        if errors:
            return errors, 500
        users.save(data)
        return user, 201


class Users(Resource):
    def get(self):
        users = models.User().find()
        return jsonify({"result": users})

    def post(self):
        users = models.User().find()
        args = request.json
        data, errors = self.validate(args)
        data["password"] = "passing"
        if errors:
            return errors, 500
        if models.User().save(data):
            return args, 201
        else:
            return "User could not be created " + str(args), 500

    def validate(self, data):
        errors = {}
        validators = {"first_name": [required],
                      "last_name": [required],
                      "username": [required,
                                   functools.partial(length, min=3)],
                      "student_no": [],
                      "home_directory": [],
                      "login_shell": [],
                      "yos": [],
                      "email": []}
        # make sure all value keys are there
        for key in validators.keys():
            try:
                value = data[key]
            except KeyError:
                data[key] = None
        # validate
        for key in validators.keys():
            value = data[key]
            field_errors = []
            for validator in validators[key]:
                try:
                    validator(value)
                except ValidationError as e:
                    field_errors.append(e.message)
            if field_errors:
                errors[key] = field_errors
        return data, errors
