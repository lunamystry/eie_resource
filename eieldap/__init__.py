import os
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
for location in os.curdir, "/etc/eieldap":
    try:
        with open(os.path.join(location, "eieldaprc")) as source:
            config.readfp(source)
    except IOError:
        print "Configuration not found, Searched: " + location
