import os
import json
import logging
import logging.config
from ConfigParser import SafeConfigParser

# I call these service variables, they're essential global variables
# for the package


def setup_logging(
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
        default_path='/etc/eie_config/eieldap.cfg',
        env_key='RESOURCE_LOG_CFG'
        ):
    """Setup application configuration

    """
    config = SafeConfigParser()
    path = default_path
    if os.path.exists(path):
        with open(path) as source:
            config.readfp(source)
    else:
        error_msg = "{} does not exist".format(path)
        logging.error(error_msg)
        raise IOError(error_msg)
    return config

_setup_logging()
config = _setup_app()

from eieldap.manager import Manager
manager = Manager(config)
