from flask import render_template
from flask import redirect
from flask import send_from_directory
from backend import app
from backend import rest
from backend import api
import os
import logging


logger = logging.getLogger(__name__)

api.add_resource(rest.Users, '/users')
api.add_resource(rest.User, '/users/<string:username>')
# api.add_resource(rest.ChangePassword,
#                  '/users/<string:username>/set_password')
# api.add_resource(rest.ResetPassword,
# '/users/<string:username>/reset_password')
api.add_resource(rest.Groups, '/groups')
api.add_resource(rest.Group, '/groups/<string:group_name>')
api.add_resource(rest.Images, '/images')
api.add_resource(rest.Image, '/images/<string:id>')
api.add_resource(rest.Sessions, '/sessions')
api.add_resource(rest.Session, '/sessions/<string:session_id>')
api.add_resource(rest.Computers, '/computers')
api.add_resource(rest.Computer, '/computers/<string:computer_id>')
api.add_resource(rest.Bookings, '/bookings')
api.add_resource(rest.Booking, '/bookings/<string:booking_id>')


@app.route('/')
@app.route('/index.html')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('templates/404.html'), 404


@app.route('/docs/')
def documentation_index():
    return redirect("/docs/index.html")


@app.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logger.info("CWD: " + cwd)
    return send_from_directory(cwd + '/../docs/build/html/', filename)


@app.errorhandler(500)
def internal_error(error):
    return render_template('templates/500.html'), 500
