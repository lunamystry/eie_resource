from flask import request,render_template,session,flash,url_for,redirect
from flask.views import MethodView
import Forms

class LoginManager(MethodView):
    def get(self):
        form = Forms.LoginForm(request.form,csrf_enabled=False)
        return render_template('login.haml',form=form)

    def post(self):
        error = None
        form = Forms.LoginForm(request.form,csrf_enabled=False)
        if request.form['username'] != 'raduser':
            error = 'Problem with username or password'
        elif request.form['password'] != 'pass':
            error = 'Problem with username or password'
        else:
            session['user_uid'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('index'))
        return render_template('login.haml',form=form, error=error)
  
class Users(MethodView):
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            return render_template('hello.haml',name="Stranger")
        else:
            # expose a single user
            return render_template('hello.haml',name=user_id)

    def post(self):
        form = Forms.NewUserForm(request.form,csrf_enabled=False)


    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

class Machines(MethodView):
    def get(self, machine_id):
        if machine_id is None:
            # return a list of machines
            pass
        else:
            # expose a single machine
            pass

    def post(self):
        # create a new machines
        pass

    def delete(self, user_id):
        # delete a single machine
        pass

    def put(self, user_id):
        # update a single machine
        pass
