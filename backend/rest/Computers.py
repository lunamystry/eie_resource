from flask import request
from flask.ext.restful import Resource
import logging
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

    def put(self, computer_id):
        args = request.json
        computer = client.resource.computers.find_one({
            '_id': ObjectId(computer_id)})
        if computer:
            del args['_id']
            for key in args:
                computer[key] = args[key]
            client.resource.computers.save(computer)
            computer["_id"] = str(computer["_id"])
            return computer, 200
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

    def to_macs(self, computers):
        """
            input: list of computers
            return: string mac address list for clonezilla
        """
        macs = ""
        for computer in computers:
            mac = "# {0} {1} {2} \n{3}\n".format(computer['number'],
                                                 computer['name'],
                                                 computer['comment'],
                                                 computer['mac'])
            macs += mac.lstrip()
        return macs

    def to_dhcp_conf(self, computers):
        """
            input: list of computers
            return: dhcp.conf formated list
        """
        dhcp_conf = ""
        for computer in computers:
            host = ("host {name} {{ \n"
                    "  ddns-hostname {name} \n"
                    "  fixed-address {ipv4} \n"
                    "  hardware ethernet {mac} \n"
                    "}}").format(**computer)
            dhcp_conf += host.rjust(2, ' ')
        return dhcp_conf

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
