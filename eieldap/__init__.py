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
        logging.basicConfig(level=default_level)

config = SafeConfigParser()
for location in os.curdir, "/etc/eie_config":
    try:
        with open(os.path.join(location, "eieldaprc")) as source:
            config.readfp(source)
    except IOError:
        logging.error(" No application configuration in: " + location)
    try:
        setup_logging()
    except IOError:
        logging.error(" No logging configuration in: " + location)


from eieldap.manager import Manager
manager = Manager(config)
