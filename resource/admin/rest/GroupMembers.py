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


class GroupMember(Resource):
    def get(self, group_name, username):
        """ This should use the Users model to return a
        user's info who is the group"""
        # group = models.GroupMembers().find_one({"id": group_name})
        return group_name

    def delete(self, group_id):
        group = models.GroupMembers().find_one({"id": group_id})
        models.GroupMembers().delete(group["name"]);
        return "", 200

    def put(self, group_id):
        app.logger.error("PUT NOT IMPLEMENTED FOR GroupMember.py")
        return group_id, 500


class GroupMembers(Resource):
    def get(self, group_name):
        """ Lets see all the members in a group """
        groups = models.groups.find_one(group_name)
        return jsonify({"result": groups})

    def post(self, group_name):
        """ Add a member to a group """
        app.logger.info("Trying to create a group... chotto matte kudasai")
        args = request.json
        group = models.groups.find_one(group_name)
        data, errors = self.validate(args)
        return jsonify({"result":group})
        # if errors:
        #     return errors, 400
        # if models.GroupMembers().save(data):
        #     return args, 201
        # else:
        #     return "GroupMember could not be created " + str(args), 500

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
