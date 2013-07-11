import os
# import manager
# import models
# import xlstoldif

config= None

# config= None
# for loc in os.curdir, os.path.expanduser("~"), "/etc/myproject", os.environ.get("MYPROJECT_CONF"):
#     try:
#         with open(os.path.join(loc,"myproject.conf")) as source:
#             config.readfp( source )
#     except IOError:
#         pass

for loc in os.curdir, "/etc/eieldap":
    try:
        with open(os.path.join(loc,".eieldaprc")) as source:
            print(source)
            # config.readfp( source )
    except IOError:
        pass

# manager = Manager(source)
