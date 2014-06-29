from flask import redirect
from flask import send_from_directory
import os
from backend.admin import admin
import logging

logger = logging.getLogger("backend.admin.routes")


@admin.route('/docs/')
def documentation_index():
    return redirect("/admin/docs/index.html")


@admin.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    logger.info("CWD: " + cwd)
    return send_from_directory(cwd + '/../../docs/build/html/', filename)
