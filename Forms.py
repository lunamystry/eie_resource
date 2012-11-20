from flask.ext.wtf import Form, TextField, Required

class RegistrationForm(Form):
    name = TextField("Name", validators=[Required()])
    student_number = TextField("Student number", validators=[Required()])
    yos = TextField("Year of study", validators=[Required()])
    email = TextField("email", validators=[Required()])
    mac = TextField("mac address", validators=[Required()])
    domain = TextField("Domain", validators=[Required()])
    supervisor_name = TextField("Supervisor Name", validators=[Required()])
    supervisor_email = TextField("Supervisor email", validators=[Required()])

class LockerRegistrationForm(Form):
    name = TextField("Name", validators=[Required()])
    student_number = TextField("Student number", validators=[Required()])
    email = TextField("email", validators=[Required()])
