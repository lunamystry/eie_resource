from flask import render_template
from flask import request
from flask import send_from_directory
import os
from resource.admin import admin
from resource.admin import RestAPI
from resource import api
import logging

api.add_resource(RestAPI.Users, '/users')
api.add_resource(RestAPI.User, '/users/<string:user_id>')

@admin.before_request
def restrict_bp_to_admins():
    #if not users.is_current_user_admin():
    #    return redirect(users.create_login_url(request.url))
    pass


@admin.route('/', defaults={'page': 'index'})
@admin.route('/<page>')
def index(page):
    return render_template('index.haml')


@admin.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logging.info("CWD: " + cwd)
    return send_from_directory(cwd + '/static/docs', filename)


@admin.route('/js/<path:filename>')
def js(filename):
    cwd = os.path.dirname(__file__)
    return send_from_directory(cwd + '/static/js', filename)
