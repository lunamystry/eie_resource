from flask import render_template
from flask import request
from flask import send_from_directory
import os
from resource.admin import admin
from resource.admin import rest
from resource import api
import logging

api.add_resource(rest.Users, '/users')
api.add_resource(rest.User, '/users/<string:user_id>')
api.add_resource(rest.Groups, '/groups')
api.add_resource(rest.GroupMembers, '/groups/<string:group_name>')
api.add_resource(rest.GroupMember,
                 '/groups/<string:group_name>/<string:username>')


@admin.before_request
def restrict_bp_to_admins():
    # if not users.is_current_user_admin():
    #    return redirect(users.create_login_url(request.url))
    pass

@admin.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logging.info("CWD: " + cwd)
    return send_from_directory(cwd + '/static/docs', filename)


@admin.route('/<path:filename>')
def index(filename):
    cwd = os.path.dirname(__file__)
    logging.info("CWD: " + cwd)
    return send_from_directory(cwd + '/static/frontend', filename)
