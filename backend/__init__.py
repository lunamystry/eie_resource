from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.restful import Api
import os
import json
import logging
import logging.config


def _setup_logging(
        default_path='/etc/eie_config/logging_config.json',
        default_level=logging.DEBUG,
        env_key='RESOURCE_LOG_CFG'
        ):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.loads(f.read())
        logging.config.dictConfig(config)
    else:
        error_msg = "{} does not exist".format(path)
        logging.warn(error_msg)
        logging.basicConfig(level=default_level)


def _setup_app(
        default_path='/etc/eie_config/resource.cfg',
        env_key='RESOURCE_LOG_CFG'
        ):
    """Setup application configuration

    """
    app = Flask(__name__,
                template_folder='../frontend/views',
                static_url_path='',
                static_folder='../frontend')
    path = default_path
    if os.path.exists(path):
        app.config.from_pyfile(path)
    else:
        error_msg = "{} does not exist".format(path)
        logging.error(error_msg)
        raise IOError(error_msg)
    return app


_setup_logging()
app = _setup_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)

from backend import routes
