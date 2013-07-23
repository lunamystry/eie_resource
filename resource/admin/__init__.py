from flask import Blueprint
from flask import redirect, request

admin = Blueprint('admin',
               __name__,
               template_folder='templates',
               static_folder='static')

import resource.admin.routes
