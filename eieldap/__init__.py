import os
import logging
import logging.config
from ConfigParser import SafeConfigParser

# I call these service variables, they're essential global variables
# for the package

config = SafeConfigParser()
for location in os.curdir, "/etc/eie_config":
    try:
        with open(os.path.join(location, "eieldap.cfg")) as source:
            config.readfp(source)
    except IOError:
        logging.debug(" * No application configuration in: " + location)
    try:
        with open(os.path.join(location, "logrc")) as source:
            logging.config.fileConfig(source)
    except IOError:
        logging.debug(" * No logging configuration in: " + location)

logger = logging.getLogger("eieldap")

from eieldap.manager import Manager
manager = Manager(config)
