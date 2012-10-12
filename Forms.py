from flask.ext.wtf import Form, TextField, Required

class RegistrationForm(Form):
    name = TextField("Name", validators=[Required()])
    email = TextField("email", validators=[Required()])
    mac = TextField("mac address", validators=[Required()])
    domain = TextField("Domain", validators=[Required()])
    supervisor_name = TextField("Supervisor Name", validators=[Required()])
    supervisor_email = TextField("email", validators=[Required()])
