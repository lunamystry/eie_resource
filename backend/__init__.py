from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.restful import Api
import os


app = Flask(__name__,
            template_folder='../frontend/views',
            static_url_path='',
            static_folder='../frontend')


config_dir = "/etc/eie_config"
try:
    filename = os.path.join(config_dir, "resource.cfg")
    with open(filename) as source:
        app.config.from_pyfile(filename)
except IOError:
    app.logger.error("No application configuration in: " + config_dir)


app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)
config = app.config

from backend import routes
