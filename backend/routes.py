from flask import render_template
from backend import app
from backend import rest
from backend import api
import logging

logger = logging.getLogger("backend.routes")

api.add_resource(rest.ClassPhotos, '/class_photos')
api.add_resource(rest.ClassPhoto, '/class_photos/<string:name>')
api.add_resource(rest.Sessions, '/sessions')
api.add_resource(rest.Session, '/sessions/<string:session_id>')
api.add_resource(rest.Password, '/passwords/<string:username>/<string:session_key>')


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
