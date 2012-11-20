from flask import Flask,url_for,render_template,request
from werkzeug import ImmutableDict
from hamlish_jinja import HamlishExtension

import Forms

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
    		extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    		)

app = FlaskWithHamlish(__name__)

@app.route('/')
def index():
    return render_template('index.haml')
    # return render_template('notice.html')

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name != None:
       return render_template('hello.html',name=name)
    else:
       return 'Hello stranger.'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

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

if __name__ == '__main__':
    app.jinja_env.hamlish_mode = 'indented'
    app.debug = True
    app.secret_key = "@*ry$ecre#"
    app.run(host='0.0.0.0',port=81)
