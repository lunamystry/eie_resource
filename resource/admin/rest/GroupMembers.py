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
        group = models.groups.find_one(group_name)
        if group:
            return {"result": group['members']}, 201
        else:
            return group, 404

    def delete(self, group_name, username):
        group = models.groups.find_one(group_name)
        if group:
            models.groups.delete(group_name)
            return "", 200


class GroupMembers(Resource):
    def get(self, group_name):
        """ Lets see all the members in a group """
        groups = models.groups.find_one(group_name)
        return jsonify({"result": [groups]})

    def post(self, group_name):
        """ Add a member to a group """
        app.logger.info("Trying to create a group... chotto matte kudasai")
        args = request.json
        data, errors = self.validate(args)
        group = models.groups.find_one(group_name)
        if errors:
            return errors, 400
        if group:
            models.groups.add_member(group['name'], data['username'])
            return {"result": [group]}, 201
        else:
            return "{} could not get added to group ".format(args), 500

    def validate(self, data):
        errors = {}
        validators = {"username": [required]}
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
