from flask import request
from flask.ext.restful import Resource
import functools
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.validators import find_errors

client = MongoClient()
logger = logging.getLogger(__name__)


def checked_for_errors(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        values = request.json
        required = ['contact_person', 'dates', 'computers', 'software',
                    'demis']
        errors = find_errors(values, required)
        if errors:
            logger.warning(str(errors))
            return errors, 400
        return f(*args, **kwargs)
    return decorated


class Booking(Resource):
    def get(self, booking_id):
        booking = client.resource.bookings.find_one({
            '_id': ObjectId(booking_id)})
        if booking:
            booking["_id"] = str(booking["_id"])
            return booking
        return "{'booking': 'Booking not found'}", 404

    @checked_for_errors
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

    @checked_for_errors
    def post(self):
        booking = request.json
        # client.resource.bookings.save(booking)
        # booking['_id'] = str(booking['_id'])
        return booking, 201
