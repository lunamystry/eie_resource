from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.restful import Api
import os


app = Flask(__name__,
            template_folder='../frontend/guest',
            static_url_path='',
            static_folder='../frontend/guest')


for location in ["/etc/eieldap"]:
    try:
        filename = os.path.join(location, "resource.cfg")
        with open(filename) as source:
            app.config.from_pyfile(filename)
    except IOError:
        app.logger.error(" * No application configuration in: " + location)


if os.environ.get('RESOURCE_SETTINGS') is not None:
    app.logger.info("using configuration in from RESOURCE_SETTINGS ")
    app.config.from_envvar('RESOURCE_SETTINGS')


app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)


from backend import routes
import admin
app.register_blueprint(admin.admin, url_prefix='/admin')
