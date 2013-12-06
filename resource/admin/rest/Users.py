from flask import request
from flask import jsonify
from flask.views import MethodView
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import abort
import functools
from resource.validators import required
from resource.validators import length
from resource.validators import ValidationError
from eieldap.models import users
from eieldap import logger


class User(Resource):
    def get(self, username):
        user = users.find_one(username)
        return user

    def put(self, username):
        user = users.find_one(username)
        args = request.json
        # TODO: Validation!
        data, errors = validate(args)
        if user:
            # TODO:  Move this line to the model
            if 'new_password' in args.keys():
                users.change_password(user_id,
                                      None,
                                      args['new_password'])
        else:
            logger.info(args)
        if errors:
            return errors, 500
        if users.save(data):
            return user, 201
        return False, 500

    def delete(self, username):
        if users.delete(username):
            return username, 200


class Users(Resource):
    def get(self):
        user_list = users.find()
        return user_list, 200

    def post(self):
        # users = users.find()
        args = request.json
        data, errors = validate(args)
        logger.error(data)
        data["password"] = "passing"
        if errors:
            return errors, 500
        if users.save(data):
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
