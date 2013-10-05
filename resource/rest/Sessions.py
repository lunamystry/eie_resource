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
from eieldap import models
from eieldap import logger

client = MongoClient()

class Session(Resource):
    def get(self, session_id):
        session = client.resource.sessions.find_one({
            'id': ObjectId(session_id)})
        if self.is_active(session):
            session["id"] = str(session["id"])
            return session
        else:
            return "{'session': 'Session not found'}", 404

    def delete(self, session_id):
        client.resource.sessions.remove({'id': ObjectId(session_id)})
        return "", 204

    def put(self, session_id):
        session = client.resource.sessions.find_one({
            'id': ObjectId(session_id)})
        args = request.json
        for key in args.keys():
            session[key] = args[key]
        client.resource.sessions.save(session)
        session["id"] = str(session["id"])
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
        which is the session key stored mongodb"""
        args = request.json
        data, errors = self.validate(args)
        if errors:
            return errors, 500
        user = models.User().find_one({'username': data["username"]})
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
        return models.User().authenticate(username, password)

    def hashed(self, password, salt):
        return hashlib.sha512(password + salt).hexdigest()
