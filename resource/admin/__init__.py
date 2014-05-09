from flask import Blueprint

admin = Blueprint('admin',
                  __name__,
                  template_folder='../../frontend/admin',
                  static_url_path='',
                  static_folder='../../frontend/admin')

import resource.admin.routes
