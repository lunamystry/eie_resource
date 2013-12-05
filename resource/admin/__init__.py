from flask import Blueprint

admin = Blueprint('admin',
                  __name__,
                  template_folder='frontend/app',
                  static_url_path='',
                  static_folder='frontend/app')

import resource.admin.routes
