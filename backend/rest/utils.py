from flask import request
from flask import abort
import functools
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from eieldap.models import groups

client = MongoClient()
logger = logging.getLogger(__name__)


def admin_only(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check if the authentication header is set
        if "x-auth-key" not in request.headers:
            logger.error('missing headers')
            return "missing headers", 400
        session = client.resource.sessions.find_one({
            '_id': ObjectId(request.headers['x-auth-key'])})
        if not session:
            return "unauthorized", 401
        admin_group = groups.find("IT")
        if not admin_group:
            logger.error("IT group does not exist")
            abort(500)
        if session['username'] not in admin_group['members']:
            error_msg = '{} is not an admin'.format(session['username'])
            logger.error(error_msg)
            return "unauthorized", 401
        return f(*args, **kwargs)
    return decorated
