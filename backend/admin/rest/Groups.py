from flask import request
from flask import jsonify
from flask.views import MethodView
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import abort
import functools
from resource import app
from resource.validators import required
from resource.validators import length
from resource.validators import ValidationError
from eieldap import models
from eieldap import logger


class Group(Resource):
    def get(self, group_name):
        group = models.groups.find_one(group_name)
        return group

    def delete(self, group_name):
        group = models.groups.find_one(group_name)
        if group:
            models.groups.delete(group_name);
        return group_name, 200


class Groups(Resource):
    def get(self):
        groups = models.groups.find()
        return jsonify({"result": groups})

    def post(self):
        """ Create a new Group, must provide only Name """
        app.logger.info("Trying to create a group... joto mate")
        args = request.json
        data, errors = self.validate(args)
        if errors:
            return errors, 400
        if models.groups.save(data):
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
