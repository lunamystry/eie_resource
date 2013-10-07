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
    def get(self, user_id):
        user = models.User().find_one({"username": user_id})
        return user

    def delete(self, user_id):
        logger.error("NOT IMPLEMENTED")
        return "", 500

    def put(self, user_id):
        user = models.User().find_one({"username": user_id})
        args = request.json
        # TODO: Validation!
        # data, errors = Users().validate(args)
        if user:
            if 'new_password' in args.keys():
                models.User().change_password(user_id,
                                              None,
                                              args['new_password'])
            else:
                logger.info(args)
        # if errors:
        #     return errors, 500
        # users.save(data)
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
