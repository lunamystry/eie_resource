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
from eieldap import models
from eieldap import logger


class User(Resource):
    def get(self, username):
        user = models.users.find_one(username)
        return user

    def put(self, username):
        user = models.users.find_one(username)
        args = request.json
        # TODO: Validation!
        data, errors = users.validate(args)
        if user:
            if 'new_password' in args.keys():
                models.users.change_password(user_id,
                                              None,
                                              args['new_password'])
            else:
                logger.info(args)
        if errors:
            return errors, 500
        if models.users.save(data):
            return user, 201
        return False, 500

    def delete(self, username):
        if models.users.delete(username):
            return username, 200


class Users(Resource):
    def get(self):
        users = models.users.find()
        return users, 200

    def post(self):
        # users = models.users.find()
        args = request.json
        data, errors = self.validate(args)
        logger.error(data)
        data["password"] = "passing"
        if errors:
            return errors, 500
        if models.users.save(data):
            return args, 201
        else:
            return "User could not be created " + str(args), 500

    def validate(self, data):
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
