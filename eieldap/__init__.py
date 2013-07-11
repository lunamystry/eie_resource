import os
# import manager
# import models
# import xlstoldif

config= None
for loc in os.curdir, "/etc/eieldap":
    try:
        with open(os.path.join(loc,".eieldaprc")) as source:
            config.readfp( source )
    except IOError:
        pass

print config
# manager = Manager(source)
