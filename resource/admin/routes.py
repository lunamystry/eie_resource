from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
import os
from resource.admin import admin
from resource.admin import rest
from resource import api
from resource import login_manager
from flask.ext.login import login_required
import logging

api.add_resource(rest.Users, '/users')
api.add_resource(rest.User, '/users/<string:username>')
api.add_resource(rest.Groups, '/groups')
api.add_resource(rest.GroupMembers, '/groups/<string:group_name>')
api.add_resource(rest.GroupMember, '/groups/<string:group_name>/<string:username>')


@admin.before_request
def restrict_bp_to_admins():
    # if not users.is_current_user_admin():
    #    return redirect(users.create_login_url(request.url))
    pass


@admin.route('/')
@admin.route('/index.html')
def index():
    return admin.send_static_file('index.html')


@admin.route('/docs/')
@login_required
def index_documentation():
    return redirect("/admin/docs/index.html")


@admin.route('/docs/<path:filename>')
@login_required
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logging.info("CWD: " + cwd)
    return send_from_directory(cwd + '/static/docs', filename)


# @admin.route('/<path:filename>')
# @login_required
# def index(filename):
#     cwd = os.path.dirname(__file__)
#     logging.info("CWD: " + cwd)
#     return send_from_directory(cwd + '/static/frontend', filename)
