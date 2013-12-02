from eieldap.models import users

user = {"username": "guneap",
        "first_name": "Gunea",
        "last_name": "Pig",
        "email": ["gunea.pig@students.wits.ac.za"],
        "password": "passing",
        "hosts": ['babbage.ug.eie.wits.ac.za',
                  'testing.ug.eie.wits.ac.za',
                    'volt.eie.wits.ac.za'],
        "yos": "4"}

if users.save(user):
    print "Saved"
