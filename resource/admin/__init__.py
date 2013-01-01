from flask import Blueprint
from flask import redirect, request

bp = Blueprint('admin', __name__)

import resource.admin.routes
