from flask import redirect
from flask import send_from_directory
import os
from backend.admin import admin
from backend.admin import rest
from backend import api
import logging

logger = logging.getLogger("backend.admin.routes")


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
