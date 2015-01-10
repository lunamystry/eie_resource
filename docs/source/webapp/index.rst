Resource Dlab Webapp
====================

Installation
------------

The resource front in developed using Flask. Flask is best install using the
Python package install pip.
To install pip run the following commands:
This is a minted python code::

        curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py my_new_env
        . my_new_env/bin/activate
        pip install

More documentation can be found here:
`<http://www.pip-installer.org/en/latest/installing.html>`_

Also need to install hamlish_jinja and flask-wtf
flask
hamlish_jinja
flask-wtf

You need to run python version 27 for flask to work
It works with git aswell. Currently on Mandla's github repo.

Setting dev environment
-----------------------

Its worth looking at the Openldap documentation for how ldap works.
Python-ldap has this doc site:
`<http://www.python-ldap.org/docs.shtml>`_

RESTful API
-----------

Users
+++++

GET /users?start=5&limit=14

    Returns not more than 14 users starting with the fifth one, this depends on
    the users, if there aren't enough users, the ones who are found are
    returned. If the start point is after the number of users then zero is
    returned.

GET /user/johnd

    Get the user with username johnd

PUT /users/johnd

    Modify a user which has username username johnd, password cannot be changed
    like this. To change password see below. The password field is simply
    removed from the json object.

PUT /users/johnd/resetpassword

    Reset the password for an individual user with username  johnd

PUT /users/johnd/set_password

    Change the password for an individual user with username  johnd

DELETE /users/johnd

    Delete a user with username johnd

POST /users

    This takes a list which contains one to many users. If the list is empty, a
    400 status code is returned. The current value in the database is replaced
    with the value given.

.. toctree::
   :maxdepth: 2
