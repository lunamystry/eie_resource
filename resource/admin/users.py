from flask import request,render_template,session,flash,url_for,redirect
from flask.ext.wtf import Form, TextField, PasswordField, Required
from flask.views import MethodView

class View(MethodView):
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

class ChangePasswordForm(Form):
    current_password = PasswordField("Current Password", validators=[Required()])
    new_password = PasswordField("New Password", validators=[Required()])
    new_password2 = PasswordField("Confirm Password", validators=[Required()])

class NewUserForm(Form):
    name = TextField("Name", validators=[Required()])
    student_number = TextField("Student number", validators=[Required()])
    # there should be a 1/2, 2/3, 3/4 for cross curriculum
    yos = TextField("Year of study", validators=[Required()])
    email = TextField("email", validators=[Required()])
    # password will be auto set by the system

