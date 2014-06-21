from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
import functools
import logging
from backend.validators import required
from backend.validators import length
from backend.validators import ValidationError
from eieldap.models import users
from utils import admin_only

logger = logging.getLogger("backend.admin.rest.Users")


class ChangePassword(Resource):
    def put(self, username):
        args = request.json
        # Talk about weak security!
        if users.change_password(username,
                                 None,
                                 args['new_password']):
            return True, 201
        else:
            return {}, 500


class ResetPassword(Resource):
    def put(self, username):
        if users.reset_password(username):
            return True, 201
        else:
            return {}, 500


class User(Resource):
    def get(self, username):
        user = users.find_one(username)
        return user

    def put(self, username):
        user = users.find_one(username)
        args = request.json
        # TODO: Validation!
        if user:
            for key, val in args.iteritems():
                user[key] = val
            if users.update(user):
                return user, 201
        else:
            logger.warning("user "+username+" not found")
        return False, 500

    @admin_only
    def delete(self, username):
        users.delete(str(username))
        return username, 200


class Users(Resource):
    @admin_only
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int, help='start must be a number')
        parser.add_argument('limit', type=int, help='limit must be a number')
        args = parser.parse_args()
        start = args["start"]
        limit = args["limit"]
        user_list = users.find()[start:][:limit]
        return user_list, 200

    @admin_only
    def post(self):
        # users = users.find()
        args = request.json
        data, errors = validate(args)
        data["password"] = "passing"
        if errors:
            return errors, 500
        if users.update(data):
            return args, 201
        else:
            return "User could not be created " + str(args), 500


def validate(data):
    errors = {}
    validators = {"first_name": [required],
                  "last_name": [required],
                  "username": [required,
                               functools.partial(length, min=3)],
                  "student_number": [],
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