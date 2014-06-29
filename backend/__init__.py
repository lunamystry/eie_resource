from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.restful import Api
import os


app = Flask(__name__,
            template_folder='../frontend/views',
            static_url_path='',
            static_folder='../frontend')




app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)
config = app.config

from backend import routes
