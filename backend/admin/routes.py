from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
import os
from backend.admin import admin
from backend.admin import rest
from backend import api
from backend import login_manager
from backend.rest import Sessions
from flask.ext.login import login_required
from eieldap.models import users
from eieldap.models import groups
import logging

logger = logging.getLogger("backend.admin.routes")

api.add_resource(rest.Users, '/users')
api.add_resource(rest.User, '/users/<string:username>')
api.add_resource(rest.ChangePassword, '/users/<string:username>/change_password')
api.add_resource(rest.ResetPassword, '/users/<string:username>/reset_password')
api.add_resource(rest.Groups, '/groups')
api.add_resource(rest.GroupMembers, '/groups/<string:group_name>')
api.add_resource(rest.GroupMember, '/groups/<string:group_name>/<string:username>')


@admin.before_request
def restrict_to_admins():
    pass
    # logger.info(request.headers)
    # session_key = request.session_id
    # username = Session().get(session_key).username
    # IT_group = groups.find_one('IT')
    # if not IT_group:
    #     logger.error("Trying to authenticate but server does not have IT group");
    #     abort(500)
    # if username not in IT_group['members']:
    #     abort(403)


@admin.route('/')
# @login_required
@admin.route('/index.html')
def index():
    return admin.send_static_file('index.html')


@admin.route('/docs/')
# @login_required
def documentation_index():
    return redirect("/admin/docs/index.html")


@admin.route('/docs/<path:filename>')
# @login_required
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logger.info("CWD: " + cwd)
    return send_from_directory(cwd + '/../../docs/build/html/', filename)
