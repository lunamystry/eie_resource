from flask import request
from flask.ext.restful import abort
import functools
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
logger = logging.getLogger("backend.admin.utils")


def admin_only(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check if the authentication header is set
        if "x-auth-key" not in request.headers:
            abort(401)
        logger.info("get session: "+str(request.headers['x-auth-key']))
        session = client.resource.sessions.find_one({
            '_id': ObjectId(request.headers['x-auth-key'])})
        if not session:
            abort(401)
        # Check if the person who the key belongs to is admin
        logger.info(session)
        return f(*args, **kwargs)
    return decorated
