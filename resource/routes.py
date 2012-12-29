from flask import url_for,render_template,request
from resource import app

import Forms

@app.route('/')
def index():
    return render_template('index.haml')
    # return render_template('notice.html')

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.haml',name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.haml'), 404

@app.route('/get_ipaddress', methods=['GET', 'POST'])
def get_ipaddress():
    # TODO: Why does csrf not work remotely
    form = Forms.RegistrationForm(request.form,csrf_enabled=False)
    return render_template('ipaddress_form.haml',form=form)

@app.route('/lockers', methods=['GET', 'POST'])
def get_locker():
    form = Forms.LockerRegistrationForm(request.form,csrf_enabled=False)
    return render_template('locker_form.haml',form=form)

@app.route('/dlab_bookings', methods=['GET', 'POST'])
def get_locker():
    form = Forms.DlabBookingForm(request.form,csrf_enabled=False)
    return render_template('dlab_booking_form.haml',form=form)
