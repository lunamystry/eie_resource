from flask import url_for,render_template,request, redirect, flash
from resource import app

import forms

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
    form = forms.DomainRegistrationForm(request.form)
    if form.validate_on_submit():
        flash('You will get an IP address if you qualify')
        return redirect('/')
    return render_template('ipaddress_form.haml',form=form,title="get an ipaddress")

@app.route('/lockers', methods=['GET', 'POST'])
def get_locker():
    form = forms.LockerRegistrationForm(request.form,csrf_enabled=False)
    return render_template('locker_form.haml',form=form)

@app.route('/dlab_bookings', methods=['GET', 'POST'])
def get_locker():
    form = forms.DlabBookingForm(request.form,csrf_enabled=False)
    return render_template('dlab_booking_form.haml',form=form)
