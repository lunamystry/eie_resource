from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
import functools
import logging
from eieldap import users
from utils import admin_only


logger = logging.getLogger(__name__)


class User(Resource):
    def get(self, username):
        user = users.User.find(username).as_dict()
        return user

    @admin_only
    def post(self, username):
        args = request.json
        try:
            username = str(args['username'])
            year_of_study = int(args['yos'])
            password = users.default_password
        except KeyError as e:
            return str(e), 500
        try:
            user = users.User(username, year_of_study, password)
            user.create()
            for key, value in args.items():
                if key == 'year_of_study':
                    setattr(user, key, int(value))
                elif key != 'username':
                    setattr(user, key, str(value))
            user.save()
        except ValueError as e:
            return str(e), 500
        return args, 201

    def put(self, username):
        user = users.User.find(username)
        args = request.json
        # TODO: Validation!
        if user:
            for key, value in args.items():
                if key == 'year_of_study':
                    setattr(user, key, int(value))
                elif key != 'username':
                    print(key,value)
                    setattr(user, key, str(value))
            user.update()
            return user.as_dict(), 201
        else:
            logger.warning("user "+username+" not found")
            return username + " not found", 404
        return False, 500

    @admin_only
    def delete(self, username):
        users.User.delete(str(username))
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
        user_list = []
        for user in users.User.find()[start:][:limit]:
            user_list.append(user.as_dict())
        return user_list, 200


def validate(data):
    pass
    # errors = {}
    # validators = {"first_name": [required],
    #               "last_name": [required],
    #               "username": [required,
    #                            functools.partial(length, min=3)],
    #               "student_number": [],
    #               "home_directory": [],
    #               "login_shell": [],
    #               "yos": [],
    #               "email": []}
    # # make sure all value keys are there
    # for key in validators.keys():
    #     try:
    #         value = data[key]
    #     except KeyError:
    #         data[key] = None
    # # validate
    # for key in validators.keys():
    #     value = data[key]
    #     field_errors = []
    #     for validator in validators[key]:
    #         try:
    #             validator(value)
    #         except ValidationError as e:
    #             field_errors.append(e.message)
    #     if field_errors:
    #         errors[key] = field_errors
    # return data, errors
