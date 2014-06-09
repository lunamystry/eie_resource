from flask import request
from flask import jsonify
from flask.ext.restful import Resource
import uuid
import logging
import hashlib
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.validators import required
from backend.validators import ValidationError
from eieldap.models import users

client = MongoClient()
logger = logging.getLogger("backend.rest.Sessions")


class Session(Resource):
    def get(self, session_id):
        session = client.resource.sessions.find_one({
            '_id': ObjectId(session_id)})
        if session:
            if self.is_active(session):
                session["_id"] = str(session["_id"])
                return session
            else:
                client.resource.sessions.remove({'_id': ObjectId(session_id)})
        return "{'session': 'Session not found'}", 401

    def delete(self, session_id):
        client.resource.sessions.remove({'_id': ObjectId(session_id)})
        return "{'result': 'Deleted session'}", 205

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
        return session_list

    def post(self):
        """ Login means POSTing to this, this checks the credentials
        If they are valid, it returns a temporary uuid (not very secure)
        which is the session key stored mongodb"""
        args = request.json
        data, errors = self.validate(args)
        if errors:
            return errors, 401
        user = users.find_one(data["username"])

        if(self.authenticate(data["username"], data["password"])):
            session = client.resource.sessions.find_one({
                "username": str(user["username"])})
            if not session:
                session = {"username": str(user["username"])}
            session["key"] = str(uuid.uuid4())
            session["timestamp"] = str(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            client.resource.sessions.save(session)
            session['_id'] = str(session['_id'])
            return jsonify({"result": session})
        return {"username": "Username or Password error", "password": "Username or Password error"}, 401

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
        return users.authenticate(username, password)

    def hashed(self, password, salt):
        return hashlib.sha512(password + salt).hexdigest()
