from flask import request
from flask.ext.restful import Resource
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.validators import find_errors

client = MongoClient()
logger = logging.getLogger(__name__)


class Booking(Resource):
    def get(self, booking_id):
        booking = client.resource.bookings.find_one({
            '_id': ObjectId(booking_id)})
        if booking:
            booking["_id"] = str(booking["_id"])
            return booking
        return "{'booking': 'Booking not found'}", 404

    def put(self, booking_id):
        args = request.json
        booking = client.resource.bookings.find_one({
            '_id': ObjectId(booking_id)})
        if booking:
            del args['_id']
            for key in args:
                booking[key] = args[key]
            client.resource.bookings.save(booking)
            booking["_id"] = str(booking["_id"])
            return booking, 200
        return "{'booking': 'Booking not found'}", 404

    def delete(self, booking_id):
        client.resource.bookings.remove({'_id': ObjectId(booking_id)})
        return "{'result': 'Deleted booking'}", 205


class Bookings(Resource):
    def get(self):
        booking_collection = client.resource.bookings
        bookings = [booking for booking in booking_collection.find()]
        for booking in bookings:
            booking["_id"] = str(booking["_id"])
        return bookings

    def post(self):
        args = request.json
        booking = self.add_missing(args)
        errors = self.find_errors(booking)
        if errors:
            return errors, 400

        client.resource.bookings.save(booking)
        booking['_id'] = str(booking['_id'])
        return booking, 201

    def add_missing(args):
        pass

    def find_errors(self, args):
        required = ['contact_person', 'dates', 'computers', 'software',
                    'demis', 'comment']
        return find_errors(args, required)
