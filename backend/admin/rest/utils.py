from flask import request
from flask.ext.restful import abort
import functools
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from eieldap.models import groups

client = MongoClient()
logger = logging.getLogger("backend.admin.utils")


def admin_only(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check if the authentication header is set
        if "x-auth-key" not in request.headers:
            abort(401)
        logger.info("get session: " + str(request.headers['x-auth-key']))
        session = client.resource.sessions.find_one({
            '_id': ObjectId(request.headers['x-auth-key'])})
        if not session:
            abort(401)
        admin_group = groups.find("IT")
        if admin_group:
            logger.info(admin_group)
        else:
            logger.error("IT group does not exist")
            abort(500)
        if session['username'] not in admin_group['members']:
            abort(401)
        return f(*args, **kwargs)
    return decorated
