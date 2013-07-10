from flask import Flask
from flask.ext.restful import Api
from werkzeug import ImmutableDict
from hamlish_jinja import HamlishExtension

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'hamlish_jinja.HamlishExtension'])

app = FlaskWithHamlish(__name__)
app.config.from_object('resource.default_settings')
app.config.from_envvar('RESOURCE_SETTINGS')
# mandatory config
app.jinja_env.hamlish_mode = 'indented'
api = Api(app)

from resource import routes
import admin
app.register_blueprint(admin.bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
