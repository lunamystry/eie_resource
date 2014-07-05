from flask import request
from flask.ext.restful import reqparse
from flask.ext.restful import Resource
from backend import app
from backend.validators import required
from backend.validators import ValidationError
from eieldap.models import groups
from utils import admin_only
import logging


logger = logging.getLogger('backend.admin.rest.Groups')


class Group(Resource):
    def get(self, group_name):
        group = groups.find_one(group_name)
        return group

    @admin_only
    def delete(self, group_name):
        group = groups.find_one(group_name)
        if group:
            groups.delete(group_name)
        return group_name, 200


class Groups(Resource):
    @admin_only
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int, help='start must be a number')
        parser.add_argument('limit', type=int, help='limit must be a number')
        args = parser.parse_args()
        start = args["start"]
        limit = args["limit"]
        group_list = groups.find()[start:][:limit]
        return group_list, 200

    @admin_only
    def post(self):
        """ Create a new Group, must provide only Name """
        app.logger.info("Trying to create a group... joto mate")
        args = request.json
        data, errors = self.validate(args)
        if errors:
            logger.error(errors)
            return errors, 400
        if groups.save(data):
            return args, 201
        else:
            return "Group could not be created " + str(args), 500

    def validate(self, data):
        errors = {}
        validators = {"name": [required], "members": [required]}
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
