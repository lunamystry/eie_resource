#! /usr/bin/env python
from resource import app

app.jinja_env.hamlish_mode = 'indented'
app.debug = True
app.secret_key = "@*ry$ecre#"
app.run(host='0.0.0.0',port=3000)
