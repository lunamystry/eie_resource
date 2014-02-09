from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import url_for
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUser,
                             confirm_login, fresh_login_required)
import os
from resource import app
from resource import login_manager
from resource import rest
from resource import admin
from resource import api
from eieldap.models import users, groups


api.add_resource(rest.ClassPhotos, '/class_photos')
api.add_resource(rest.ClassPhoto, '/class_photos/<string:name>')
api.add_resource(rest.Sessions, '/sessions')
api.add_resource(rest.Session, '/sessions/<string:session_id>')
api.add_resource(rest.Password, '/passwords/<string:username>/<string:session_key>')


@app.route('/')
@app.route('/index.html')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('templates/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('templates/500.html'), 500


# LOGIN -----------------------------------------------

class User(UserMixin):
    def __init__(self, username):
        self.attributes = users.find_one(username)
        self.username = username
        self.id = username

    def is_active(self):
        return True


class Anonymous(AnonymousUser):
    name = u"Anonymous"


@login_manager.user_loader
def load_user(username):
    return User(username)


@app.route("/login", methods=["GET", "POST"])
def login():
    app.logger.info("username" in request.form)
    error = None
    if request.method == "POST":
        username = request.form["username_input"]
        password = request.form["password_input"]
        if users.authenticate(username, password):
            remember = request.form.get("remember", "no") == "yes"
            remember = "no"
            if login_user(User(username), remember=remember):
                error = "Logged in"
                IT_group = groups.find_one('IT')
                if not IT_group:
                    app.logger.error("Trying to login but server does not have IT group");
                    abort(500)
                if username in IT_group['members']:
                    return redirect(request.args.get("next") or
                                    url_for("admin.index",
                                            filename="app/index.html"))
                else:
                    return redirect(request.args.get("next") or
                                    url_for("index"))
            else:
                error = "Sorry, but you could not log in."
        error = "Incorrect password of username."
    return app.send_static_file('index.html')


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
