from flask import url_for,render_template,request
from resource.admin import bp

@bp.before_request
def restrict_bp_to_admins():
    #if not users.is_current_user_admin():
    #    return redirect(users.create_login_url(request.url))
    pass

@bp.route('/', defaults={'page': 'index'})
@bp.route('/<page>')
def admin(page):
    return "Admin ages will go here!"
