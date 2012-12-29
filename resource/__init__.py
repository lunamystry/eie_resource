from flask import Flask
from werkzeug import ImmutableDict
from hamlish_jinja import HamlishExtension

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
    		extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    		)

app = FlaskWithHamlish(__name__)

import resource.routes

if __name__ == '__main__':
    app.jinja_env.hamlish_mode = 'indented'
    app.debug = True
    app.secret_key = "@*ry$ecre#"
    app.run(host='0.0.0.0')
