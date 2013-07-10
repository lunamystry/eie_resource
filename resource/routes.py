from flask import render_template
from flask import request
from flask import send_from_directory
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import abort
from resource import RestAPI
from resource import app
from resource import api

api.add_resource(RestAPI.Sessions, '/sessions')
api.add_resource(RestAPI.Session, '/sessions/<string:session_id>')


@app.route('/')
def index():
    return render_template('index.haml')
    # return render_template('notice.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.haml'), 404


@app.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    return send_from_directory(cwd + '/static/docs', filename)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.haml'), 500
