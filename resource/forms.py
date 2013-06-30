from flask.ext.wtf import Form
from flask.ext.wtf import TextField
from flask.ext.wtf import Required


class DomainRegistrationForm(Form):
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
    yos = TextField("Year of study", validators=[Required()])


class DlabBookingForm(Form):
    name = TextField("Name", validators=[Required()])
    person_number = TextField("Person number", validators=[Required()])
    email = TextField("email", validators=[Required()])
    role = TextField("Role", validators=[Required()])
    forwhat = TextField("For what", validators=[Required()])
    date = TextField("Date", validators=[Required()])
    start_time = TextField("Start time", validators=[Required()])
    end_time = TextField("End time", validators=[Required()])
    pcs = TextField("Number of PCs", validators=[Required()])
    notes = TextField("Special requirements", validators=[Required()])
