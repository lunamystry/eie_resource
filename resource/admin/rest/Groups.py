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
    def get(self, group_id):
        group = models.Groups().find_one({"id": group_id})
        return group

    def delete(self, group_id):
        group = models.Groups().find_one({"id": group_id})
        models.Groups().delete(group["name"]);
        return "", 200

    def put(self, group_id):
        app.logger.error("PUT NOT IMPLEMENTED FOR Group.py")
        return group_id, 500


class Groups(Resource):
    def get(self):
        groups = models.Groups().find()
        return jsonify({"result": groups})

    def post(self):
        app.logger.info("Trying to create a group... joto mate")
        args = request.json
        all_groups = models.Groups().find()
        data, errors = self.validate(args)
        if errors:
            return errors, 400
        if models.Groups().save(data):
            return args, 201
        else:
            return "Group could not be created " + str(args), 500

    def validate(self, data):
        errors = {}
        validators = {"name": [required]}
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
