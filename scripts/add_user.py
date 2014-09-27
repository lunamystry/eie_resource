from eieldap.models import users

user = {"username": "root",
        "first_name": "Super",
        "last_name": "User",
        "email": ["root@localhost.local"],
        "password": "secret",
        "hosts": [
            'babbage.ug.eie.wits.ac.za',
            'testing.ug.eie.wits.ac.za',
            'volt.eie.wits.ac.za'
            ],
        "login_shell": "/bin/bash",
        "home_directory": "/home/ug/root",
        "yos": "4"}

users.add(user)
print "Saved"
