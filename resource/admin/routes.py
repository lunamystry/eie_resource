from flask import url_for
from flask import render_template
from flask import request
from resource.admin import bp
from resource.admin import RestAPI
from resource import api

api.add_resource(RestAPI.Sessions, '/admin/sessions')
api.add_resource(RestAPI.Session, '/admin/sessions/<string:session_id>')
api.add_resource(RestAPI.Users, '/users')
api.add_resource(RestAPI.User, '/users/<string:user_id>')


@bp.before_request
def restrict_bp_to_admins():
    #if not users.is_current_user_admin():
    #    return redirect(users.create_login_url(request.url))
    pass


@bp.route('/', defaults={'page': 'index'})
@bp.route('/<page>')
def index(page):
    return "Admin pages will go here!"
