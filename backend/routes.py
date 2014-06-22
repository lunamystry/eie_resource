from flask import render_template
from backend import app
from backend import rest
from backend import api
import logging

logger = logging.getLogger("backend.routes")

api.add_resource(rest.Users, '/users')
api.add_resource(rest.User, '/users/<string:username>')
# api.add_resource(rest.ChangePassword,
#                  '/users/<string:username>/change_password')
# api.add_resource(rest.ResetPassword,
# '/users/<string:username>/reset_password')
api.add_resource(rest.Groups, '/groups')
# api.add_resource(rest.GroupMembers, '/groups/<string:group_name>')
# api.add_resource(rest.GroupMember,
#                  '/groups/<string:group_name>/<string:username>')
api.add_resource(rest.Images, '/images')
api.add_resource(rest.Image, '/images/<string:id>')
api.add_resource(rest.Sessions, '/sessions')
api.add_resource(rest.Session, '/sessions/<string:session_id>')


@app.route('/')
@app.route('/index.html')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('templates/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('templates/500.html'), 500
