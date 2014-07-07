from flask import request
from flask import jsonify
from flask.ext.restful import Resource
import uuid
import logging
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.validators import required
from backend.validators import ValidationError

client = MongoClient()
logger = logging.getLogger("backend.rest.Computers")


class Computer(Resource):
    def get(self, computer_id):
        computer = client.resource.computers.find_one({
            '_id': ObjectId(computer_id)})
        if computer:
            computer["_id"] = str(computer["_id"])
            return computer
        return "{'computer': 'Computer not found'}", 404

    def delete(self, computer_id):
        client.resource.computers.remove({'_id': ObjectId(computer_id)})
        return "{'result': 'Deleted computer'}", 205


class Computers(Resource):
    def get(self):
        computers = client.resource.computers
        computer_list = [computer for computer in computers.find()]
        for computer in computer_list:
            computer["_id"] = str(computer["_id"])
        return computer_list

    def post(self):
        args = request.json
        computer, errors = self.validate(args)
        logger.info(args)
        if errors:
            return errors, 400

        client.resource.computers.save(computer)
        computer['_id'] = str(computer['_id'])
        return computer, 201

    def validate(self, args):
        errors = {}
        error = "missing information"
        try:
            required(args["mac"])
        except ValidationError:
            errors["mac"] = error
        try:
            required(args["name"])
        except ValidationError:
            errors["name"] = error
        return args, errors
