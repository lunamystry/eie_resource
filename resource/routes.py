from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from resource import app
import os

import forms

@app.route('/')
def index():
    return render_template('index.haml')
    # return render_template('notice.html')

@app.route('/dojo/dijit')
def dijit_demo(name=None):
    return render_template('dijit_demo.haml', name=name, title="Dojo diji demo")

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.haml', name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.haml'), 404

@app.route('/get_ipaddress', methods=['GET', 'POST'])
def get_ipaddress():
    # TODO: Why does csrf not work remotely
    form = forms.DomainRegistrationForm(request.form)
    if form.validate_on_submit():
        flash('You will get an IP address if you qualify')
        return redirect('/')
    return render_template('ipaddress_form.haml', form=form, title="get an ipaddress")

@app.route('/lockers', methods=['GET', 'POST'])
def get_locker():
    form = forms.LockerRegistrationForm(request.form, csrf_enabled=False)
    return render_template('locker_form.haml', form=form)

@app.route('/dlab_bookings', methods=['GET', 'POST'])
def get_locker():
    form = forms.DlabBookingForm(request.form, csrf_enabled=False)
    return render_template('dlab_booking_form.haml', form=form)

@app.route('/docs/<path:filename>')
def documentation(filename):
    cwd = os.path.dirname(__file__)
    return send_from_directory(cwd + '/static/docs', filename)
